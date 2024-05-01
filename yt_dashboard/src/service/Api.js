import axios from 'axios'

export default() => {
    let url = process.env.VUE_APP_API_URL

    let api = axios.create({
        baseURL: url,
        withCredentials: false,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFTOKEN'
    })

    api.interceptors.request.use(async config => {
        if(config.url !== 'api-token-auth' && config.url !== '/account/createe') {
            config.headers['Authorization'] = 'Token ' + localStorage.getItem('t')
        }
        return config;
    });

    api.interceptors.response.use((response) => response, (error) => {
        return Promise.reject(error);
    })

    return api
}