<template>
	<view class="page">
		<!-- 未登录提示 -->
		<view v-if="!isLogin" class="login-tip">
			<text class="tip-text">登录后才能发布项目</text>
			<button class="btn-primary go-btn" @click="goMine">去登录</button>
		</view>

		<!-- 发布表单 -->
		<view v-else>
			<view class="card">
				<text class="label">项目标题</text>
				<input class="input" v-model="form.title" placeholder="请输入标题" />

				<text class="label">项目简介（列表页展示）</text>
				<textarea class="textarea" v-model="form.summary" placeholder="一句话介绍项目" />

				<text class="label">详细介绍</text>
				<textarea class="textarea tall" v-model="form.detail" placeholder="详细介绍项目内容、技术、亮点等" />
			</view>

			<view class="card">
				<text class="label">封面图</text>
				<view class="cover-box" @click="chooseCover">
					<image v-if="form.cover_url" class="cover" :src="fullUrl(form.cover_url)" mode="aspectFill"></image>
					<text v-else class="plus">+ 选择封面</text>
				</view>

				<text class="label">详情图片（可多张）</text>
				<view class="imgs">
					<view class="img-item" v-for="(img, i) in form.images" :key="i">
						<image class="img" :src="fullUrl(img)" mode="aspectFill"></image>
						<text class="del" @click="removeImg(i)">×</text>
					</view>
					<view class="img-item add" @click="chooseImages">+</view>
				</view>
			</view>

			<button class="btn-primary submit" :disabled="submitting" @click="submit">
				{{ submitting ? '发布中…' : '发布项目' }}
			</button>
		</view>
	</view>
</template>

<script>
	import { request, uploadImage, getUser } from '../../utils/request.js'
	import { fullUrl } from '../../utils/config.js'

	export default {
		data() {
			return {
				isLogin: false,
				form: { title: '', summary: '', detail: '', cover_url: '', images: [] },
				submitting: false
			}
		},
		onShow() {
			this.isLogin = !!getUser()
		},
		methods: {
			fullUrl,
			goMine() {
				uni.switchTab({ url: '/pages/mine/mine' })
			},
			chooseCover() {
				uni.chooseImage({
					count: 1,
					success: async (res) => {
						const url = await this.upload(res.tempFilePaths[0])
						if (url) this.form.cover_url = url
					}
				})
			},
			chooseImages() {
				uni.chooseImage({
					count: 9 - this.form.images.length,
					success: async (res) => {
						for (const p of res.tempFilePaths) {
							const url = await this.upload(p)
							if (url) this.form.images.push(url)
						}
					}
				})
			},
			async upload(filePath) {
				uni.showLoading({ title: '上传中' })
				try {
					return await uploadImage(filePath)
				} catch (e) {
					return ''
				} finally {
					uni.hideLoading()
				}
			},
			removeImg(i) {
				this.form.images.splice(i, 1)
			},
			async submit() {
				if (!this.form.title.trim()) return uni.showToast({ title: '请填写标题', icon: 'none' })
				if (!this.form.summary.trim()) return uni.showToast({ title: '请填写简介', icon: 'none' })
				if (!this.form.detail.trim()) return uni.showToast({ title: '请填写详情', icon: 'none' })

				this.submitting = true
				try {
					await request({ url: '/api/projects', method: 'POST', data: this.form })
					uni.showToast({ title: '发布成功', icon: 'success' })
					this.form = { title: '', summary: '', detail: '', cover_url: '', images: [] }
					setTimeout(() => uni.switchTab({ url: '/pages/index/index' }), 800)
				} catch (e) {}
				this.submitting = false
			}
		}
	}
</script>

<style scoped>
	.login-tip {
		padding-top: 200rpx;
		text-align: center;
	}
	.tip-text {
		display: block;
		color: #999;
		margin-bottom: 30rpx;
	}
	.go-btn {
		width: 300rpx;
	}
	.label {
		display: block;
		font-size: 28rpx;
		font-weight: bold;
		margin: 20rpx 0 10rpx;
	}
	.input {
		background: #f5f6f8;
		border-radius: 12rpx;
		height: 80rpx;
		padding: 0 20rpx;
		font-size: 28rpx;
	}
	.textarea {
		background: #f5f6f8;
		border-radius: 12rpx;
		width: 100%;
		height: 140rpx;
		padding: 16rpx 20rpx;
		font-size: 28rpx;
		box-sizing: border-box;
	}
	.textarea.tall {
		height: 300rpx;
	}
	.cover-box {
		width: 300rpx;
		height: 200rpx;
		border-radius: 12rpx;
		background: #f5f6f8;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}
	.cover {
		width: 100%;
		height: 100%;
	}
	.plus {
		color: #9ca3af;
		font-size: 28rpx;
	}
	.imgs {
		display: flex;
		flex-wrap: wrap;
	}
	.img-item {
		width: 200rpx;
		height: 200rpx;
		margin: 0 16rpx 16rpx 0;
		border-radius: 12rpx;
		overflow: hidden;
		position: relative;
	}
	.img {
		width: 100%;
		height: 100%;
	}
	.img-item.add {
		background: #f5f6f8;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 60rpx;
		color: #9ca3af;
	}
	.del {
		position: absolute;
		top: 0;
		right: 0;
		width: 44rpx;
		height: 44rpx;
		background: rgba(0, 0, 0, 0.5);
		color: #fff;
		text-align: center;
		line-height: 44rpx;
		border-radius: 0 0 0 12rpx;
		font-size: 30rpx;
	}
	.submit {
		margin-top: 20rpx;
	}
</style>
