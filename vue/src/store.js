import { defineStore } from 'pinia';
import axios from 'axios'
import { router } from './router';


export const useMainStore = defineStore('main', {
    state: () => ({
        apiBaseUrl: import.meta.env.MODE === 'production'
            ? '/taskhub'
            : 'http://localhost:60000',
        user: null,
        demoUser: null,
        selectedTeam: null
    }),
    persist: [
        {
            paths: ['user'],
            storage: sessionStorage
        },
        {
            paths: ['selectedTeam'],
            storage: sessionStorage
        }
    ],
    getters: {
        api: (state) => {
            return {
                get: (endpoint, params = {}) => {
                    return axios.get(state.apiBaseUrl + endpoint, {
                        params,
                        withCredentials: true
                    });
                },
                post: (endpoint, data) => {
                    return axios.post(state.apiBaseUrl + endpoint, data, {
                        withCredentials: true
                    });
                },
                put: (endpoint, data) => {
                    return axios.put(state.apiBaseUrl + endpoint, data, {
                        withCredentials: true
                    });
                },
                delete: (endpoint) => {
                    return axios.delete(state.apiBaseUrl + endpoint, {
                        withCredentials: true
                    });
                }
            };
        },
        isLoggedIn: (state) => {
            return state.user !== null
        }
    },
    actions: {
        setUser(user) {
            this.user = user;
        },
        setSelectedTeam(team) {
            this.selectedTeam = team
        },
        setDemoUser(demo) {
            this.demoUser = demo
        },
        setupInterceptors() {
            axios.interceptors.response.use(
                (response) => response,
                async (error) => {
                    if (error.config.url.includes('/auth/token/refresh/')) {
                        console.error('Refresh token is invalid, logging out...');
                        this.setUser(null);
                        router.replace({ name: 'Login' });
                        return Promise.reject(error);
                    }

                    if ((error.response?.status === 401 || error.response?.status === 403) && !error.config._retry) {
                        error.config._retry = true;

                        try {
                            await axios.post(this.apiBaseUrl + '/auth/token/refresh/', null, {
                                withCredentials: true
                            });
                            return axios(error.config);
                        } catch (refreshError) {
                            return Promise.reject(refreshError);
                        }
                    }

                    return Promise.reject(error);
                }
            );
        }
    }
});