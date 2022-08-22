import api from './api/axios'

async function upload(formData, query) {
    return api.post('/files/xls/upload?tag=' + query, formData, {
        headers: {
            "Access-Control-Allow-Origin": "http://localhost:8000",
            "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token",
            "Content-Type": "multipart/form-data"
        },
        responseType: 'blob'
    }).then((response) => {
        return response;
    })
}

export { upload };