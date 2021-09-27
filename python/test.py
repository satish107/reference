# ____*____
# ___***___
# __*****__
# _*******_
# *********

n=20
for i in range(1, 11):
    print(' '*n, end='') # repet space for n times
    print('* '*(i)) # repeat stars for i times
    n-=1



    // $('.carousel-control-next, .carousel-control-prev').click(function(){
    //     var chapter_name = $('.carousel-item.active').data('chapter');
    //     var concept_weight = $('.carousel-item.active').data('conceptweight');
    //     var concept_index = $('.carousel-item.active').data('index');
    //     $('#flashcards-counter').text(concept_index)
    //     $('#chapter_name').text(chapter_name)

    // });

    $('.carousel-control-next').click(function(){
        var chapter_name = $('.carousel-item.active').next().data('chapter');
        var concept_index = $('.carousel-item.active').next().data('index');
        if (chapter_name == null){
            var chapter_name = $('.carousel-item:first').data('chapter');
            var concept_index = $('.carousel-item:first').data('index');
            $('#flashcards-counter').text(concept_index)
            $('#chapter_name').text(chapter_name)
        }
        $('#flashcards-counter').text(concept_index)
        $('#chapter_name').text(chapter_name)
    });

    $('.carousel-control-prev').click(function(){
        var chapter_name = $('.carousel-item.active').prev().data('chapter');
        var concept_index = $('.carousel-item.active').prev().data('index');
        if (chapter_name == null){
            var chapter_name = $('.carousel-item:last').data('chapter');
            var concept_index = $('.carousel-item:last').data('index');
            $('#chapter_name').text(chapter_name)
            $('#flashcards-counter').text(concept_index)
        }
        $('#flashcards-counter').text(concept_index)
        $('#chapter_name').text(chapter_name)
    });



if(reset_concept != "None"){
        	var reset_concept_id = "{{last_active_user_concept.concept.id}}"
	        var reset_chapter_name = "{{last_active_user_concept.concept.chapter.name}}"
	        var reset_carousel_index = $(`[data-conceptid=${reset_concept_id}]`).data('index');
	        $('#custCarousel').carousel(reset_carousel_index - 1);
	        $('#chapter_name').text(reset_chapter_name);
	        $('#flashcards-counter').text(reset_carousel_index);
        }



if UserProfile.objects.filter(email=request.data.get('email')).exists():
	user = UserProfile.objects.filter(email=request.data.get('email')).last()
	if level:
		level = Level.objects.get(id=level)
		user.level = level
	if education_interest:
		education_interest = EducationInterest.objects.get(id=education_interest)
		user.education_interest = education_interest
	if exams_id:
		for exam_id in exams_id:
			exam = Exam.objects.get(id=exam_id)
			if not UserExamDate.objects.filter(user=user).exists():
				UserExamDate.objects.create(user=user, exam=exam, date=exam.date)
	user.save()
	user.refresh_from_db()
else:
	serializer = serializers.UserSerializer(data=request.data)
	if serializer.is_valid():
		user = UserProfile.objects.create(
			email=request.data.get('email'),
			name=request.data.get('name'),
			phone_number=request.data.get('phone_number')
		)
		password = request.data.get('password')
		user.set_password(password)
		user.save()

		token, created = Token.objects.get_or_create(user=user)

	if level:
		level = Level.objects.get(id=level)
		user.level = level

	if education_interest:
		education_interest = EducationInterest.objects.get(id=education_interest)
		user.education_interest = education_interest

	if exams_id:
		for exam_id in exams_id:
			exam = Exam.objects.get(id=exam_id)
			UserExamDate.objects.create(user=user, exam=exam, date=exam.date)
	user.save()

	user.refresh_from_db()

This behaviour is the source of the following dependency conflicts.
django-storages 1.10.1 requires Django>=2.2, but you have django 1.11.20 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
google-cloud-firestore 2.0.2 requires google-api-core[grpc]<2.0.0dev,>=1.22.1, but you have google-api-core 1.16.0 which is incompatible.
google-cloud-core 1.4.4 requires google-api-core<2.0.0dev,>=1.21.0, but you have google-api-core 1.16.0 which is incompatible.
google-api-python-client 1.12.8 requires google-api-core<2dev,>=1.21.0, but you have google-api-core 1.16.0 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
firebase-admin 2.18.0 requires google-api-python-client>=1.7.8, but you have google-api-python-client 1.6.7 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
firebase-admin 2.18.0 requires google-api-python-client>=1.7.8, but you have google-api-python-client 1.6.7 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
google-cloud-storage 1.34.0 requires google-cloud-core<2.0dev,>=1.4.1, but you have google-cloud-core 1.3.0 which is incompatible.
google-cloud-firestore 2.0.2 requires google-api-core[grpc]<2.0.0dev,>=1.22.1, but you have google-api-core 1.16.0 which is incompatible.
google-cloud-firestore 2.0.2 requires google-cloud-core<2.0dev,>=1.4.1, but you have google-cloud-core 1.3.0 which is incompatible.
firebase-admin 2.18.0 requires google-api-python-client>=1.7.8, but you have google-api-python-client 1.6.7 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
proto-plus 1.13.0 requires protobuf>=3.12.0, but you have protobuf 3.6.1 which is incompatible.
firebase-admin 2.18.0 requires google-api-python-client>=1.7.8, but you have google-api-python-client 1.6.7 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
pylint-django 2.0.12 requires pylint>=2.0, but you have pylint 1.9.5 which is incompatible.
prospector 1.2.0 requires astroid==2.3.3, but you have astroid 1.6.6 which is incompatible.
prospector 1.2.0 requires pylint==2.4.4, but you have pylint 1.9.5 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
prospector 1.2.0 requires astroid==2.3.3, but you have astroid 1.6.6 which is incompatible.
prospector 1.2.0 requires pylint==2.4.4, but you have pylint 1.9.5 which is incompatible.
prospector 1.2.0 requires pylint-django==2.0.12, but you have pylint-django 0.8.1 which is incompatible

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
gdshortener 1.0.1 requires requests>=2.21.0, but you have requests 2.18.4 which is incompatible.
firebase-admin 2.18.0 requires google-api-python-client>=1.7.8, but you have google-api-python-client 1.6.7 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
user-agents 2.2.0 requires ua-parser>=0.10.0, but you have ua-parser 0.9.0 which is incompatible.



# if UserTimeTable.objects.filter(user=request.user, parent_exam=exam_parent, sellable_product_group=sellable_product_group).exists():

# 	user_time_table = UserTimeTable.objects.filter(user=request.user, parent_exam=exam_parent, sellable_product_group=sellable_product_group)

# 	user_time_table_started = user_time_table.filter(status=2, chapter_exam__in=user_products)
# 	total_subjects = user_time_table.values_list('subject_id', flat=True).distinct()
# 	time_table_new = []
# 	for subject in total_subjects:
# 		user_time_table_first = user_time_table.filter(status=1, subject=subject).first()
# 		time_table_new.append(user_time_table_first)

# 	context = {
# 		'exam_parent_id': exam_parent.id,
# 		'user_id': request.user.id,
# 		'sellable_product_group_id': sellable_product_group.id,
# 	}
# 	response_dict['exam_name'] = exam_parent.short_name
# 	response_dict['time_table'] = serializers.UserTimeTableSerializer(time_table_new, context=context, many=True).data

# else:
# 	ai_time_table_service = AITimeTableService(user=request.user, exam_parent=exam_parent, sellable_product_group=sellable_product_group)
# 	ai_time_table_service.get_or_create_user_time_table()
# 	print('user time table does not exists')


# # return Response({'status':'ok'})
# return SuccessResponse(response_dict)


user_time_table_new = []
		if user_time_table.filter(chapter_exam__in=user_products, status=2).exists():
			print('status 2')
			user_time_table_started = user_time_table.filter(chapter_exam__in=user_products, status=2)
			total_subjects = user_time_table_started.values_list('subject_id', flat=True).distinct()
			print(total_subjects)
			for subject in total_subjects:
				user_time_table_first = user_time_table_started.filter).first()
				user_time_table_new.append(user_time_table_first)

		elif user_time_table.filter(chapter_exam__in=user_products, status=1).exists():
			print('status 1')
			total_subjects = user_time_table_started.values_list('subject_id', flat=True).distinct()
			user_time_table_todo = user_time_table.filter(chapter_exam__in=user_products, status=1)
			print(total_subjects)
			for subject in total_subjects:
				user_time_table_first = user_time_table_todo.first()
				user_time_table_new.append(user_time_table_first)



class ChatApi(APIView):

	authentication_classes = (
		authentication.TokenAuthentication,
		authentication.SessionAuthentication
	)

	permission_classes = [permissions.IsAuthenticated, ApiKeyPermission]

	def get(self, request, version, format=None):

		chat_room_id = request.GET.get('chat_room_id')

		chat_messages = ChatMessage.objects.filter(chat_room_id=chat_room_id)
		chat_messages_serializer = serializers.ChatMessageSerializer(chat_messages, many=True).data

		return SuccessResponse(chat_messages_serializer)

	def get_my_correct_questions(self, obj):
		end_date = datetime.datetime.now().date()
		start_date = end_date - timedelta(days=6)
		dates = []
		for i in range(7):
			date = start_date + timedelta(days=i)
			dates.append(date)
		correct_questions = OrderedDict()
		for date in dates:
			number_correct_questions = OrderedDict()
			my_correct_questions = obj.objects.filter(user=obj.user, added_on__date=date, user_test__sellable_product_group=sellable_product_group, option_status=1).count()
			others_correct_questions = obj.objects.filter(added_on__date=date, user_test__sellable_product_group=sellable_product_group, option_status=1).exclude(user=obj.user).count()
			distinct_users = obj.objects.filter(added_on__date=date, user_test__sellable_product_group=sellable_product_group, option_status=1).exclude(user=obj.user).values('user_id').distinct().count()
			if distinct_users:
				others_correct_questions_avg = others_correct_questions / distinct_users
			else:
				others_correct_questions_avg = 0
			number_correct_questions['my_correct_questions'] = my_correct_questions
			number_correct_questions['others_correct_questions_avg'] = others_correct_questions_avg
			correct_questions[str(date)] = number_correct_questions
		return correct_questions

		ai_coach_user_feed = AICoachUserFeed.objects.filter(sellable_product_group=sellable_product_group)
		user_test_analysis = UserTestAnalysis.objects.filter(user_test__sellable_product_group=sellable_product_group)
		time_studying_ai_coach = []
		number_of_correct_questions_list = []
		for date in dates:

			study_performance_time_dict = OrderedDict()
			my_time_spent = ai_coach_user_feed.filter(user=request.user, added_on__date=date).aggregate(sum=Sum('time_spent_absolute'))['sum'] or 0
			others_time_spent = ai_coach_user_feed.filter(added_on__date=date).exclude(user=request.user).values('user_id').distinct().aggregate(avg=Avg('time_spent_absolute'))['avg'] or 0
			time_spent = OrderedDict()
			time_spent['my_time_spent'] = my_time_spent
			time_spent['others_time_spent'] = others_time_spent
			study_performance_time_dict[str(date)] = time_spent
			time_studying_ai_coach.append(study_performance_time_dict)

			correct_question_dict = OrderedDict()
			my_correct_questions = user_test_analysis.filter(user=request.user, added_on__date=date).aggregate(sum=Sum('correct_questions'))['sum'] or 0
			others_correct_questions = user_test_analysis.filter(added_on__date=date).exclude(user=request.user).aggregate(avg=Avg('correct_questions'))['avg'] or 0
			correct_questions = OrderedDict()
			correct_questions['my_correct_questions'] = my_correct_questions
			correct_questions['others_correct_questions'] = others_correct_questions
			correct_question_dict[str(date)] = correct_questions
			number_of_correct_questions_list.append(correct_question_dict)


# AICoachUserFeed.objects.filter(user_id=1, added_on__gte='29-12-2021').values('added_on__date','my_time_spent').annotate(my_time_spent=Sum('time_spent_absolute'))
# AICoachUserFeed.objects.filter(user_id=1, added_on='29-12-2021',sellable_product_group_id=56).annotate(my_time_spent=Sum('time_spent_absolute'))
# UserTestQuestion.objects.filter(user_id=1, added_on='29-12-2021', user_test__sellable_product_group=sellable_product_group, option_status=1).count()


class UserTimeTableApi(APIView):

	authentication_classes = (
		authentication.TokenAuthentication,
		authentication.SessionAuthentication
	)

	permission_classes = [permissions.IsAuthenticated, ApiKeyPermission]

	def get(self, request, version, format=None):

		exam_id = self.request.query_params.get('exam_id')
		if str(exam_id) == '0':
			exam_id = 1373
		exam_parent = Exam.objects.get(id=exam_id).parent_exam
		subjects = ChapterExam.objects.filter(examparent=exam_parent).values_list('chapter__subject', flat=True).distinct()
		subjects = Subject.objects.filter(id__in=subjects)
		
		response_dict = {}
		subject_time_table_list = []
		for subject in subjects:
			subject_data = OrderedDict()
			subject_data['id'] = subject.id
			subject_data['name'] = subject.name
			image = ''
			if subject.image_location:
				image += settings.STATIC_URL + str(subject.image_location)
			subject_data['image'] = image
			subject_wise_time_table = UserTimeTable.objects.filter(user=request.user, parent_exam=exam_parent, subject=subject)
			time_table_serializer = serializers.UserTimeTableSerializer(subject_wise_time_table, many=True).data
			subject_data['time_table'] = time_table_serializer
			subject_time_table_list.append(subject_data)

		return SuccessResponse(subject_time_table_list)

date.strftime("%d-%m-%Y")

git show d490bc199f35c974629b24ec03d9c9f826a78f0f # removed subject_serializer and chapter_serializer, marks from TestPrepQuestionSerializer
git show ec92e4693a7eba3d0d59446d1c8a5a7c8f546bb1 # chat api version changed
git show 6ecd1f87871edce4fcd360c72f2fc5effad2ed19 # aitimetableservice get or create timetable


if sellable_product_group.exam_parent.short_name == 'BITSAT':
	response_dict['live_classes'] = False
	response_dict['refer_and_earn'] = False
	response_dict['bookmarks'] = False




