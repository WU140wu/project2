// 后端接口基础地址
// H5 预览用 127.0.0.1 即可；真机/模拟器调试时，请改成电脑的局域网 IP，
// 例如 http://10.31.39.40:5000（电脑和手机需在同一 WiFi）
export const BASE_URL = 'http://127.0.0.1:5000'

// 把后端返回的相对路径（如 /uploads/xxx.jpg）拼成完整地址
export function fullUrl(path) {
	if (!path) return ''
	if (/^https?:\/\//.test(path)) return path
	return BASE_URL + path
}

// 把 ISO 时间转成 "YYYY-MM-DD HH:mm"
export function formatTime(iso) {
	if (!iso) return ''
	return iso.slice(0, 16).replace('T', ' ')
}
