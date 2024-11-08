import axiosInstance from "@/axios";
import { API_URL_LOGOUT, API_URL_USER_PERMISSIONS, VALIDATE_TG_INIT_DATA } from "@/constants/ada-api.js";

export const auth = {
    namespaced: true,
    state: () => ({
        user: null,
        userPermissions: [],
    }),
    mutations: {
        SET_USER(state, user) {
            state.user = user;
        },
        CLEAR_USER(state) {
            state.user = null;
        },
        SET_USER_PERMISSIONS(state, permissions) {
            state.userPermissions = permissions;
        },
        CLEAR_USER_PERMISSIONS(state) {
            state.userPermissions = [];
        },
    },
    actions: {
        async fetchUserPermissions({ commit }) {
            try {
                const response = await axiosInstance.get(API_URL_USER_PERMISSIONS);
                commit('SET_USER_PERMISSIONS', response.data.permissions);
            } catch (error) {
                console.error("Error fetching user permissions:", error);
                commit('SET_USER_PERMISSIONS', []);
            }
        },
        async fetchUser({ commit }, { TWA }) {
            let initData;
            if (import.meta.env.MODE === "development") {
                console.log(import.meta.env.VITE_INIT_DATA);
                initData = JSON.parse(import.meta.env.VITE_INIT_DATA);
            } else {
                initData = TWA.initData;
            }
            console.log('initData', initData);
            console.log('mode', import.meta.env.MODE);
            const initDataString = new URLSearchParams(initData).toString();
            await axiosInstance.post(VALIDATE_TG_INIT_DATA, initDataString)
                .then(response => {
                    console.log('user response', response.data.user)
                    commit('SET_USER', response.data.user);
                    this.dispatch('auth/fetchUserPermissions');
                })
                .catch(() => {
                    commit('CLEAR_USER');
                });
        },
        async logout({ commit }) {
            await axiosInstance.post(API_URL_LOGOUT, {}, { withCredentials: true })
                .then(() => {
                    commit('CLEAR_USER');
                    commit('CLEAR_USER_PERMISSIONS');
                });
        },
    },
    getters: {
        isLoggedIn: state => !!state.user,
        user: state => state.user,
        hasPermission: (state) => (permissionName) => {
            if (!state.user || !state.userPermissions) {
                return false;
            }
            return state.userPermissions.includes(permissionName);
        },
    }
};
