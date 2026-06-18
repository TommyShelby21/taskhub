import { createRouter, createWebHistory } from 'vue-router'
import { useMainStore } from './store.js'
import HomePage from './views/HomePage.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Profile from './views/Profile.vue'
import AddTeam from './views/AddTeam.vue'
import TaskOrganizator from './views/TaskOrganizator.vue'
import Team from './views/Team.vue'


const routes = [
    {
        path: '/',
        name: 'HomePage',
        component: HomePage,
        meta: { navbar: true, auth: true }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { navbar: false }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { navbar: false }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
        meta: { navbar: true, auth: true }
    },
    {
        path: '/team/:id',
        name: 'Team',
        component: Team,
        meta: { navbar: true, auth: true }
    },
    {
        path: '/team/:id/task-organizator',
        name: 'TaskOrganizator',
        component: TaskOrganizator,
        meta: { navbar: true, auth: true }
    },
    {
        path: '/add-team',
        name: 'AddTeam',
        component: AddTeam,
        meta: { navbar: true, auth: true }
    },
]

export const router = createRouter({
    history: createWebHistory('/'),
    routes,
})

router.beforeEach((to, from, next) => {
    //  TODO: SETUP AUTH GUARD HERE
    const store = useMainStore()
    if (to.fullPath === '/login' && store.isLoggedIn === true) {
        next({ name: 'HomePage' })
    }
    if (to.meta.auth && store.isLoggedIn === false && from.name !== 'Login') {
        console.log('Auth guard: not logged in, redirecting to login page')
        next({ name: 'Login' })
    }
    else {
        next()
    }
})
