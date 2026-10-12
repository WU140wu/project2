import { BASE_URL } from './config.js'

export function getToken() {
	return uni.getStorageSync('token') || ''
}

export function getUser() {
	return uni.getStorageSync('user') || null
}

export function setLogin(token, user) {
	uni.setStorageSync('token', token)
	uni.setStorageSync('user', user)
}

export function logout() {
	uni.removeStorageSync('token')
	uni.removeStorageSync('user')
}

// 统一请求封装：自动带 token，解析 {code, message, data}
export function request(options) {
	return new Promise((resolve, reject) => {
		uni.request({
			url: BASE_URL + options.url,
			method: options.method || 'GET',
			data: options.data || {},
			header: {
				'Content-Type': 'application/json',
				...(getToken() ? { Authorization: 'Bearer ' + getToken() } : {})
			},
			success: (res) => {
				const body = res.data
				if (res.statusCode === 200 && body && body.code === 0) {
					resolve(body.data)
				} else if (res.statusCode === 401) {
					logout()
					uni.showToast({ title: '请先登录', icon: 'none' })
					setTimeout(() => uni.switchTab({ url: '/pages/mine/mine' }), 600)
					reject(body)
				} else {
					uni.showToast({ title: (body && body.message) || '请求失败', icon: 'none' })
					reject(body)
				}
			},
			fail: (err) => {
				uni.showToast({ title: '网络错误，请检查后端是否启动', icon: 'none' })
				reject(err)
			}
		})
	})
}

// 上传图片，返回后端存储的相对路径 /uploads/xxx.jpg
export function uploadImage(filePath) {
	return new Promise((resolve, reject) => {
		uni.uploadFile({
			url: BASE_URL + '/api/upload',
			filePath: filePath,
			name: 'file',
			header: { Authorization: 'Bearer ' + getToken() },
			success: (res) => {
				let body
				try {
					body = JSON.parse(res.data)
				} catch (e) {
					uni.showToast({ title: '上传失败', icon: 'none' })
					reject(e)
					return
				}
				if (body.code === 0) {
					resolve(body.data.url)
				} else {
					uni.showToast({ title: body.message || '上传失败', icon: 'none' })
					reject(body)
				}
			},
			fail: (err) => {
				uni.showToast({ title: '上传失败', icon: 'none' })
				reject(err)
			}
		})
	})
}
