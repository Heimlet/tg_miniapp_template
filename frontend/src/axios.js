import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : 'http://localhost:8000/',
    // headers: {
    //     'Content-Type': 'application/x-www-form-urlencoded',
    // },
    withCredentials: true,
});

export default axiosInstance;
