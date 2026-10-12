<template>
	<view class="page">
		<!-- 已登录 -->
		<template v-if="user">
			<view class="card user-card">
				<view class="avatar">{{ (user.nickname || '?').slice(0, 1) }}</view>
				<view class="u-info">
					<text class="nickname">{{ user.nickname }}</text>
					<text class="role">{{ user.role === 'admin' ? '管理员' : '学生' }} · {{ user.username }}</text>
				</view>
				<view class="logout" @click="doLogout">退出</view>
			</view>

			<view class="card">
				<text class="section-title">我发布的项目（{{ projects.length }}）</text>
				<view class="project" v-for="p in projects" :key="p.id" @click="goDetail(p.id)">
					<text class="p-title">{{ p.title }}</text>
					<text class="p-time">{{ formatTime(p.created_at) }}</text>
				</view>
				<text v-if="!projects.length" class="empty">还没有发布项目，去「发布」试试吧</text>
			</view>
		</template>

		<!-- 未登录：登录 / 注册 -->
		<template v-else>
			<view class="card auth-card">
				<view class="tabs">
					<view class="tab" :class="{ active: mode === 'login' }" @click="mode = 'login'">登录</view>
					<view class="tab" :class="{ active: mode === 'register' }" @click="mode = 'register'">注册</view>
				</view>

				<template v-if="mode === 'login'">
					<input class="input" v-model="loginForm.username" placeholder="账号" />
					<input class="input" v-model="loginForm.password" placeholder="密码" password />
					<button class="btn-primary" @click="doLogin">登录</button>
				</template>
				<template v-else>
					<input class="input" v-model="regForm.username" placeholder="账号" />
					<input class="input" v-model="regForm.nickname" placeholder="昵称" />
					<input class="input" v-model="regForm.password" placeholder="密码（至少 6 位）" password />
					<button class="btn-primary" @click="doRegister">注册</button>
				</template>
			</view>
		</template>
	</view>
</template>

<script>
	import { request, getUser, setLogin, logout } from '../../utils/request.js'
	import { formatTime } from '../../utils/config.js'

	export default {
		data() {
			return {
				user: null,
				projects: [],
				mode: 'login',
				loginForm: { username: '', password: '' },
				regForm: { username: '', nickname: '', password: '' }
			}
		},
		onShow() {
			this.user = getUser()
			if (this.user) this.loadMine()
		},
		methods: {
			formatTime,
			async doLogin() {
				if (!this.loginForm.username || !this.loginForm.password) {
					return uni.showToast({ title: '请填写账号和密码', icon: 'none' })
				}
				try {
					const data = await request({
						url: '/api/auth/login',
						method: 'POST',
						data: this.loginForm
					})
					setLogin(data.token, data.user)
					this.user = data.user
					this.loginForm = { username: '', password: '' }
					uni.showToast({ title: '登录成功', icon: 'success' })
					this.loadMine()
				} catch (e) {}
			},
			async doRegister() {
				if (!this.regForm.username || !this.regForm.password) {
					return uni.showToast({ title: '请填写账号和密码', icon: 'none' })
				}
				if (this.regForm.password.length < 6) {
					return uni.showToast({ title: '密码至少 6 位', icon: 'none' })
				}
				try {
					await request({
						url: '/api/auth/register',
						method: 'POST',
						data: this.regForm
					})
					uni.showToast({ title: '注册成功，请登录', icon: 'success' })
					this.mode = 'login'
					this.loginForm.username = this.regForm.username
					this.loginForm.password = ''
				} catch (e) {}
			},
			async loadMine() {
				try {
					const data = await request({ url: '/api/projects/mine' })
					this.projects = data.list
				} catch (e) {}
			},
			doLogout() {
				logout()
				this.user = null
				this.projects = []
				uni.showToast({ title: '已退出', icon: 'none' })
			},
			goDetail(id) {
				uni.navigateTo({ url: '/pages/detail/detail?id=' + id })
			}
		}
	}
</script>

<style scoped>
	.user-card {
		display: flex;
		align-items: center;
	}
	.avatar {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		background: #3B82F6;
		color: #fff;
		font-size: 44rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 24rpx;
	}
	.u-info {
		flex: 1;
		display: flex;
		flex-direction: column;
	}
	.nickname {
		font-size: 34rpx;
		font-weight: bold;
	}
	.role {
		font-size: 24rpx;
		color: #999;
		margin-top: 6rpx;
	}
	.logout {
		color: #f56c6c;
		font-size: 26rpx;
		padding: 10rpx;
	}
	.project {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 24rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}
	.project:last-child {
		border-bottom: none;
	}
	.p-title {
		font-size: 28rpx;
		flex: 1;
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
	.p-time {
		font-size: 24rpx;
		color: #aaa;
		margin-left: 20rpx;
	}
	.empty {
		display: block;
		text-align: center;
		color: #999;
		padding: 30rpx 0;
	}
	.auth-card {
		margin-top: 60rpx;
	}
	.tabs {
		display: flex;
		margin-bottom: 30rpx;
	}
	.tab {
		flex: 1;
		text-align: center;
		padding: 16rpx 0;
		font-size: 30rpx;
		color: #999;
		border-bottom: 4rpx solid transparent;
	}
	.tab.active {
		color: #3B82F6;
		font-weight: bold;
		border-bottom-color: #3B82F6;
	}
	.input {
		background: #f5f6f8;
		border-radius: 12rpx;
		height: 80rpx;
		padding: 0 20rpx;
		font-size: 28rpx;
		margin-bottom: 20rpx;
	}
</style>
