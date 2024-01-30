def get_college_courses_data(college_id=None, domain_id=None, level_id=None, course_ids=None):
	# domain_level_wise_college_courses = CollegeCourseDomains.objects.filter(college_course_id__in=course_ids, domain_id=domain_id).values_list("college_course_id", flat=True)
	# college_courses = CollegeCourse.objects.filter(id__in=domain_level_wise_college_courses, level=level_id, credential__in=[None, 0, 1], published="published", status=1)
	college_courses = CollegeCourse.objects.filter(degree_domain=domain_id.id, level=level_id, credential__in=[None, 0, 1], published="published", status=1)

	college_courses_list = []
	for course in college_courses:
		if AictePlacement.objects.filter(course_id=course.id, placement__isnull=False, enrollment__isnull=False).exists():
			aicte_placement = AictePlacement.objects.select_related('course').filter(course_id=course.id, placement__isnull=False, enrollment__isnull=False).order_by('-year')
			aicte_placement_list = []
			current_year = aicte_placement.first().year
			min_year = datetime.now().year - 3
			for obj in aicte_placement:
				course_start_year = current_year - (obj.course.course_duration//12)
				placement_obj = {}
				year = obj.year
				if obj.year < min_year:
					break
		
				enrollment = None
				if aicte_placement.filter(year=course_start_year).exists() and aicte_placement.filter(Q(enrollment__isnull=False)|~Q(enrollment=''), year=course_start_year).exists():
					year = obj.year
					placement = obj.placement
					enrollment = aicte_placement.filter(year=course_start_year).last().enrollment
					percentage = (placement/enrollment)*100

					placement_obj["year"] = f"{year}-{year+1}"
					placement_obj["percentage"] = round(percentage, 2) if percentage else 0
					if not placement_obj["percentage"] == 0:
						aicte_placement_list.append(placement_obj)
			
			course_name = course.course_name
			course_dict = {}
			if len(aicte_placement_list) > 0:
				course_dict['course_id'] = course.id
				course_dict['course_name'] = course.course_name
				course_dict['placement_details'] = list(aicte_placement_list)
				college_courses_list.append(course_dict)
	return college_courses_list

def get_college_study_levels(college_id=None, domain=None, course_ids=None):
	# study_level_ids = CollegeCourseDomains.objects.filter(college_course_id__in=course_ids, domain=domain).annotate(level=F("college_course__level")).values_list("level", flat=True).distinct()
	study_level_ids = CollegeCourse.objects.filter(id__in=course_ids, degree_domain=domain.id).values_list("level", flat=True).distinct()
	study_levels = []
	for level in study_level_ids:
		course_data = get_college_courses_data(college_id=college_id, domain_id=domain, level_id=level, course_ids=course_ids)
		if len(course_data) > 0:
			study_level_dict = {}
			study_level_dict['level_name'] = PreferredEducationLevel.objects.filter(id=level).last().name
			study_level_dict['course_data'] = course_data
			study_levels.append(study_level_dict)
		return study_levels

def college_placement_graph_helper(*args, **kwargs):
	college_id = kwargs.get('college_id')
	flag = kwargs.get('flag')

	college_placement_graph_key = f"institute_{college_id}_aicte_placement_graph"
	college_detail_es_helper = CollegeDetailCachingHelper()
	aicte_placement_data = college_detail_es_helper._get_college_from_redis_by_key(college_placement_graph_key, flag=flag)

	if not aicte_placement_data:
		placement_data = []
		college_courses = CollegeCourse.objects.filter(college_id=int(college_id), credential__in=[None, 0, 1], published="published", status=1)
		current_year = datetime.now().year
		valid_year_range = [current_year, current_year - 1, current_year - 2, current_year - 3]
		aicte_placement_courses = AictePlacement.objects.filter(course_id__in=college_courses.values_list("id", flat=True), year__in=valid_year_range)
		college_courses_domains = CollegeCourse.objects.filter(id__in=aicte_placement_courses.values_list("course_id", flat=True), college_id=college_id).values_list("degree_domain", flat=True)
		domains = Domain.objects.filter(id__in=college_courses_domains)

		for domain in domains:
			domain_data = get_college_study_levels(college_id=college_id, domain=domain, course_ids=aicte_placement_courses.values_list("course_id", flat=True))
			if len(domain_data) > 0:
				domain_dict = {}
				domain_dict['domain_name'] = domain.name
				domain_dict['domain_data'] = domain_data
				placement_data.append(domain_dict)

		aicte_placement_data = placement_data
		college_detail_es_helper._create_or_update_college_from_redis_by_key(college_placement_graph_key, aicte_placement_data)

	return aicte_placement_data