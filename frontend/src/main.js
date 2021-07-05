import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "./index.css"
import vueDebounce from 'vue-debounce'

import jwt_decode from'jwt-decode'

createApp(App).use(store).use(router).use(vueDebounce).mount('#app')

let userToken = localStorage.getItem('websnap.user')
if (userToken) {
	let user = jwt_decode(userToken)
	user = user.exp * 1000 > Date.now() ? user : null
	if(user) {
		store.dispatch('login', userToken)
	}
}