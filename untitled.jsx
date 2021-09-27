import React, { useEffect, useState } from 'react';
import '@/css/etest.css';
import { BrowserView, MobileView, isBrowser, isMobile } from "react-device-detect";
import PageLayout from '../../layout/PageLayout';
// import Footer from '../../layout/partials/Footer';
import QuestionPageMob from '../../components/mobile/QuestionPageMob';
import {Tabs, Tab, Nav } from 'react-bootstrap';
import TestTabContent from '../../components/web/TestTabContent';
import { FaUserAlt } from "react-icons/fa";
import { fetchUserTest, fetchUserTestQuestion, postUserTestQuestionTime, fetchExamSummary } from '../../store/Etest/EtestActions';
import { connect } from 'react-redux';
import Loading from '../../components/common/Loader';
import { set } from 'js-cookie';
import { Link, useLocation, useParams, useHistory } from 'react-router-dom';
import {Redirect} from 'react-router';
import CommonModal from '../../components/common/CommonModal';
import TestSummaryModal from '../../components/web/TestSummaryModal';


const Test = ({ location, user, product, _user_test_data, _user_test_question, _fetchUserTest, _fetchUserTestQuestion, _postUserTestQuestionTime, _exam_summary, _fetchExamSummary }) => {

	const [open, setOpen] = useState(false)
	const [eventKey, setEventKey] = useState(0)
	// const [session, setSession] = useState(sessionStorage.getItem('test_in_progress'))
	const { userTestId, userTestQuestionId } = useParams()
	const [testTimer, setTestTimer] = useState(null)
	const [testSectionalTimer, setTestSectionalTimer] = useState(null)
	const [questionTimer, setQuestionTimer] = useState(0)
	const [questionId, setQuestionId] = useState(userTestQuestionId)
	const [examPatternSubject, setExamPatternSubject] = useState(null)
	const test_type = location.state && location.state.test_type
	const exam_parent_id = product.exam_parent
	const exam_id = product.exam.id
	const history = useHistory();
	const [submit,setSubmit]=useState(false)
	const [switchableSubjects, setSwitchableSubjects] = useState('')

	useEffect(() => {
		_fetchUserTest(product.id, exam_parent_id, exam_id, test_type)
		_fetchUserTestQuestion(userTestId, userTestQuestionId)
		setQuestionId(null)
	}, [questionId])

	if(!_user_test_question){
		return <Loading />
	}

	const all_questions = _user_test_question.all_questions
	const subjects = _user_test_question.user_test_subjects
	const current_question = _user_test_question && _user_test_question.current_question
	const exam_pattern = _user_test_question && _user_test_question.exam_pattern
	const max_section_time = _user_test_question && _user_test_question.exam_pattern && _user_test_question.exam_pattern.max_section_time
	const exam_pattern_group = _user_test_question && _user_test_question.exam_pattern_group
	const test_marking_data = _user_test_data && _user_test_data.test_marking_data

	useEffect(() => {
		if(max_section_time){
			if(sessionStorage.getItem(`test_time_sectional_remaining-${userTestId}-${exam_pattern && exam_pattern.subject_name}`)){
				setTestSectionalTimer(sessionStorage.getItem(`test_time_sectional_remaining-${userTestId}-${exam_pattern && exam_pattern.subject_name}`))
			} else {
				// if mht-cet test and test_type = 4 then sectional time is Physics+Chemistry and Maths
				if(exam_pattern_group && exam_pattern_group.length > 0 && test_type==4){
					let max_section_time = 0;
					let switchable_subjects = '';
					for(let i=0; i<exam_pattern_group.length; i++){
						max_section_time = max_section_time + (exam_pattern_group && exam_pattern_group[i].exam_pattern && exam_pattern_group[i].exam_pattern.max_section_time)
						switchable_subjects = switchable_subjects + (exam_pattern_group && exam_pattern_group[i].exam_pattern && exam_pattern_group[i].exam_pattern.subject_name)
						// setSwitchableSubjects(switchable_subjects)
					}
					if(sessionStorage.getItem(`test_time_sectional_remaining-${userTestId}-${switchable_subjects}`)){
						setTestSectionalTimer(sessionStorage.getItem(`test_time_sectional_remaining-${userTestId}-${switchable_subjects}`))
					} else{
						setTestSectionalTimer(max_section_time * 60)
					}
				} else{
					setTestSectionalTimer(exam_pattern && exam_pattern.max_section_time * 60)
				}
			}
			setExamPatternSubject(exam_pattern && exam_pattern.subject_name)
		}

		if(sessionStorage.getItem(`test_time_remaining-${userTestId}`)){
			setTestTimer(sessionStorage.getItem(`test_time_remaining-${userTestId}`))
		} else {
			setTestTimer(test_marking_data && test_marking_data.total_time * 60)
		}

		if(testTimer == (test_marking_data && test_marking_data.total_time * 60)){
			sessionStorage.setItem(`test_in_progress-${userTestId}`, true)
		}
		if(testSectionalTimer == (max_section_time * 60)){
			sessionStorage.setItem(`subject_test_in_progress-${userTestId}-${exam_pattern && exam_pattern.subject_name}`, true)
		}
		// if(!sessionStorage.getItem(`test_in_progress-${userTestId}`) || sessionStorage.getItem(`test_in_progress-${userTestId}`) == false){
		// 	history.push("/analysis/")
		// }
		if(!sessionStorage.getItem(`subject_test_in_progress-${userTestId}-${exam_pattern && exam_pattern.subject_name}`) || sessionStorage.getItem(`subject_test_in_progress-${userTestId}-${exam_pattern && exam_pattern.subject_name}`) == false){
			// Subject will Switch here
		}

		_fetchExamSummary(userTestId)
	}, [_user_test_question])


	// Main Timer
	useEffect(() => {
		let timer;
		if(testTimer > 0){
			timer = setInterval(() => setTestTimer(testTimer - 1), 1000)
		}
		sessionStorage.setItem(`test_time_remaining-${userTestId}`, testTimer)
		if(testTimer == 0){
			submitTest();
		};
		return () => clearInterval(timer)
	}, [testTimer])

	const nextSubject = (subject_id) => {
		let next_subject;
		let current_subject;
		subjects && subjects.map((subject) => {
			if(subject.id == subject_id){
				current_subject = subject
			}
		})
		let index_of_current_subject = subjects && subjects.indexOf(current_subject)
		next_subject = subjects[index_of_current_subject + 1]
		return next_subject.id
	}

	// Sectional Timer
	useEffect(() => {
		console.log("exam_pattern_group", exam_pattern_group)
		let timer;
		if(testSectionalTimer > 0){
			timer = setInterval(() => setTestSectionalTimer(testSectionalTimer - 1), 1000)
		}
		if(testSectionalTimer == 0){
			// Subject will Switch Here
			_fetchUserTestQuestion(userTestId, null, nextSubject(current_question && current_question.question && current_question.question.subject_id))
			sessionStorage.setItem(`test_time_sectional_remaining-${userTestId}-${exam_pattern && exam_pattern.subject_name}`, testSectionalTimer)
		};
		// sessionStorage.setItem(`test_time_sectional_remaining-${userTestId}-${exam_pattern && exam_pattern.subject_name}`, testSectionalTimer)
		if(exam_pattern_group && exam_pattern_group.length > 0){
			let switchable_subjects = '';
			for(let i=0; i <exam_pattern_group.length; i++){
				switchable_subjects = switchable_subjects + (exam_pattern_group && exam_pattern_group[i].exam_pattern && exam_pattern_group[i].exam_pattern.subject_name)
			}
			sessionStorage.setItem(`test_time_sectional_remaining-${userTestId}-${switchable_subjects}`, testSectionalTimer)
		} else {
			sessionStorage.setItem(`test_time_sectional_remaining-${userTestId}-${exam_pattern && exam_pattern.subject_name}`, testSectionalTimer)
		}
		return () => clearInterval(timer)
	}, [testSectionalTimer])


	useEffect(() => {
		if(open == true){
			_fetchExamSummary(userTestId)
		}
	}, [open])

	const onChangeSubject = (subject_id, index, event) => {
		console.log("exam_pattern", exam_pattern)
		console.log("test_type", test_type)
		if(exam_pattern && exam_pattern.exam_parent && exam_pattern.exam_parent.id == 541){
			if(subject_id !== current_question && current_question.question && current_question.question.subject_id){
				event.preventDefault()
				setEventKey(index)
			}
		} else if(exam_pattern && exam_pattern.exam_parent && exam_pattern.exam_parent.id == 482 && test_type == 4){
			console.log("exam_pattern", exam_pattern)
			console.log("test_type", test_type)
			console.log("subject_id", subject_id)
			if(subject_id == 3){
				console.log("................subject_id", subject_id)
				event.preventDefault()
				setEventKey(index)
			} else {
				console.log("................subject_id", subject_id)
				setEventKey(index)
				_fetchUserTestQuestion(userTestId, null, subject_id)
			}
		}
		else {
			console.log("................subject_id", subject_id)
			setEventKey(index)
			_fetchUserTestQuestion(userTestId, null, subject_id)
		}
	}

	const minutes_to_hours = (seconds) => {
		let time;
		let hours = Math.floor(seconds / 3600)
		let minutes = Math.floor((seconds - hours * 3600)/60)
		let second = (seconds - (hours * 3600) - (minutes * 60))
		if(hours < 10) {hours = "0" + hours}
		if(minutes < 10) {minutes = "0" + minutes}
		if(second < 10) {second = "0" + second}
		time = hours + ":" + minutes + ":" + second
		return time
	}
	
	const submitTest = () => {	
		setTimeout(()=>{
			sessionStorage.clear();
			history.push(`/analysis/${userTestId}`)
		},5000)
	}

  	return (
		<PageLayout title="Test">
			<BrowserView>
				<div className="test">
					<div className="container-fluid">
						<div className="row">
							<div className="col-md-9 col-sm-12">
								<div className="test-rightside">
									<div className="test-logo-careers">
										<img src={require('@/images/careers-logo.jpg')} alt="careers-logo-test" /> 
									</div>
									<div className="full-test">
										{_user_test_question && _user_test_question.user_test_name}
									</div>
									<div className="test-time">
										<div className="row">
											<div className="col-md-6">
												<h5 className="test-section">Section</h5>
											</div>
											<div className="col-md-6">
	  											<h6 className="test-time-left text-right">Time Left : <span className="test-timmer">{minutes_to_hours(testSectionalTimer ? testSectionalTimer : testTimer)}</span></h6>
											</div>
										</div>
									</div>
									<div className="test-tab-cover">
										<Tab.Container defaultActiveKey="0">
											<div className="test-tab-lists">
												<ul className="test-tab-list-items">
													{
														subjects && subjects.map((subject, index) => {
															const active_class = `test-list-item-anchor${subject.id === current_question.question.subject_id ? " test-active-list" : ""}`
															return (
																<Nav.Item><li className="test-list-items"><Nav.Link eventKey={index.toString()} onClick={(event) => {onChangeSubject(subject.id, index, event)}} className={active_class}> {subject.name}</Nav.Link></li></Nav.Item>
															)
														})
													}
												</ul>
											</div>
											<Tab.Content>
												<Tab.Pane eventKey={eventKey.toString()}>
													<TestTabContent 
														user_test_question={_user_test_question}
														submit={submit}
														flagSubmit={()=>setSubmit(false)}
													/>
												</Tab.Pane>
											</Tab.Content>
										</Tab.Container>
									</div>
								</div>
							</div>
							<div className="col-md-3 col-sm-12" style={{background: "#e7f6fd"}}>  
								<div className="test-leftside">
									<div className="test-admin">
										<div className="row">
											<div className="col-md-4">
												<div className="user-icon-test">
                                        			<FaUserAlt size={42} color="#797979" />
                                    			</div>
											</div>
											<div className="col-md-8">
												<h6 className="test-admin-heading"><b>{user.name}</b></h6>
												<p className="test-admin-text">{_user_test_data && _user_test_data.exam_pattern && _user_test_data.exam_pattern[0] && _user_test_data.exam_pattern[0]['exam_parent'] && _user_test_data.exam_pattern[0]['exam_parent'].short_name}</p>
											</div>
										</div>
									</div>
									<div className="instruction-box">
                            			<table className="instruction-area">
											<tbody>
												<tr>  
													<td><span className="answered">{_exam_summary && _exam_summary["1"]}</span></td>  
													<td>Answered</td>
													<td><span className="review">{_exam_summary && _exam_summary["3"]}</span></td>  
													<td>Marked for review.</td>
												</tr>
												<tr> 
													<td><span className="not_visited">{_exam_summary && _exam_summary["5"]}</span></td>  
													<td>Not Visited</td> 
													<td><span className="not_answered">{_exam_summary && _exam_summary["2"]}</span></td> 
													<td>Not Answered</td>  
												</tr>
												<tr>
													<td><span className="review_answered" >{_exam_summary && _exam_summary["4"]}</span></td>  
													<td colSpan="3">Answered &amp; Marked for Review <br /> (will be considered for evaluation)</td>
												</tr>
											</tbody>
										</table>
										<h4 className="test-section-subject">Section : <span>{current_question && current_question.question && current_question.question.subject_name}</span></h4>
									</div>
									
									<div className="question-numbers">
										<ul className="question-numbers-list">
											{
												all_questions && all_questions.map((question) => {
													const question_status = question.question_status
													const active_class = `${question_status === null ? "not_visited" : question_status === 1 ? "answered" : question_status === 2 ? "not_answered" : question_status === 3 ? "review" : question_status === 4 ? "review_answered" : question_status === 5 ? "not_visited" : null} auditlog`
													return (
														<li>
															<Link to={{pathname: `/testprep/test/${userTestId}/${question.id}`}} className="mark-question-status">
																<span className={active_class} onClick={() => setQuestionId(question.id)}>{question.question_no}</span>
															</Link>
														</li>
													)
												})
											}
										</ul>
									</div>
									<button type="submit" className="submit-button-answer" onClick={() => {setOpen(true);setSubmit(true)}}>
										Submit
									</button>
								</div>
							</div>
						</div>
					</div>
				</div>
				<CommonModal isOpen={open} closeModal={() => {setOpen(false);setSubmit(false)}}>
					<TestSummaryModal 
						exam_summary={_exam_summary}
						user_test_id={userTestId}
						closeExamSummaryModal={() => setOpen(false)}
						submitTest={()=>submitTest()}
					/>
				</CommonModal>
			</BrowserView>
			<MobileView>
				<QuestionPageMob 
					location={location}
					user={user}
					product={product}
					user_test_id={userTestId}
					user_test_question_id={userTestQuestionId}
					user_test_question={_user_test_question}
					submitTest={()=>submitTest()}
					exam_summary={_exam_summary}
				/>
			</MobileView>
		</PageLayout>
  	);
};

const mapStateToProps = (state) => {
	return {
		_user_test_data: state.userTestData.user_test_base,
		_user_test_question: state.userTestData.user_test_question_base,
		_exam_summary: state.userTestData.exam_summary,
	}
}

const mapDispatchToProps = (dispatch) => {
	return {
		_fetchUserTest: (sellable_product_group_id, exam_parent_id, exam_id, test_type) => dispatch(fetchUserTest(sellable_product_group_id, exam_parent_id, exam_id, test_type)),
		_fetchUserTestQuestion: (user_test_id, user_test_question_id, subject_id) => dispatch(fetchUserTestQuestion(user_test_id, user_test_question_id, subject_id)),
		_postUserTestQuestionTime: (user_test_question_id, time_spent) => dispatch(postUserTestQuestionTime(user_test_question_id, time_spent)),
		_fetchExamSummary: (user_test_id) => dispatch(fetchExamSummary(user_test_id))
	}
}

export default connect(mapStateToProps, mapDispatchToProps) (Test);
