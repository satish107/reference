// Error Boungary
static getDerivedStateFromError(error){
	return {}
}

componentDidCatch(error, info){
	console.log(error)
}

// Higher Order Components

useEffect() // replaces the use of compountDidMount(), compountDidUpdate(), compountWillUnmount() used in class based component

useReduces(reducer, initial_state)
reducer(current_state, action)

array1 = [1,2,3,4,5]
reducer = array1.reduce(first_argument, second_argument) => {first_argument + second_argument}
array1.reduce()


// data fetching using useState and useEffect
function DataFetching() {
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState('')
	const [post, setPost] = useState({})

	useEffect(() => {
		axios.get('www.test.com/1')
		.then(response => {
			setLoading(false)
			setPost(response.data)
			setError('')
		})
		.catch(error => {
			setLoading(false)
			setPost({})
			setError('Something went wrong')
		})
	}, [])

}

// data fetching Using useReducer and useEffect

const initialState = {
	loading: false,
	post: {},
	error: ''
}

const reducer(state, action) => {
	Switch(action.type){
		case 'fetching_seccess':
			return {
				loading: false,
				error: '',
				post: action.payload
			}
		case 'fetching_error':
			return {
				loading: false,
				error: 'Something went wrong',
				post: {}
			}
		default:
			return state
	}
}

function DataFetchingTwo(){
	const [state, dispatch] = useReducer(reducer, initialState)

	useEffect(() => {
		axios.get('www.test.com/1')
		.then(response => {
			dispatch({type: 'fetching_seccess', payload: response.data})
		})
		.catch(error => {
			dispatch({type: 'fetching_error'})
		})
	}, [])

	return (
		
	)

}


useState = (number, string, or boolean), (one or two state)
useReducer = (array or object), (too many state) 

useCallBack * used for performance optimization

const incrementAge = useCallBack(() => {
	setAge(age + 1)
}, [age])

// useCallBack for cache function
// useMemo for cache result


