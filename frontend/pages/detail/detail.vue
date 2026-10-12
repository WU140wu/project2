<template>
	<view class="page" v-if="project">
		<image v-if="project.cover_url" class="cover" :src="fullUrl(project.cover_url)" mode="aspectFill"></image>

		<view class="card">
			<text class="title">{{ project.title }}</text>
			<view class="meta">
				<text class="author">{{ project.author ? project.author.nickname : '匿名' }}</text>
				<text class="time">{{ formatTime(project.created_at) }}</text>
			</view>
		</view>

		<view class="card">
			<text class="section-title">项目简介</text>
			<text class="summary">{{ project.summary }}</text>
		</view>

		<view class="card">
			<text class="section-title">详细介绍</text>
			<text class="detail">{{ project.detail }}</text>
		</view>

		<view class="card" v-if="project.images && project.images.length">
			<text class="section-title">图片展示</text>
			<view class="imgs">
				<image v-for="(img, i) in project.images" :key="i" class="img" :src="fullUrl(img)" mode="aspectFill" @click="preview(i)"></image>
			</view>
		</view>

		<view class="card">
			<text class="section-title">评论（{{ comments.length }}）</text>
			<view class="comment" v-for="c in comments" :key="c.id">
				<view class="c-head">
					<text class="c-name">{{ c.author ? c.author.nickname : '匿名' }}</text>
					<text class="c-time">{{ formatTime(c.created_at) }}</text>
				</view>
				<text class="c-content">{{ c.content }}</text>
			</view>
			<view v-if="!comments.length" class="empty">暂无评论，来抢沙发～</view>
		</view>

		<!-- 底部评论输入 -->
		<view class="comment-bar">
			<input class="c-input" v-model="commentText" placeholder="写下你的评论…" confirm-type="send" @confirm="submitComment" />
			<view class="c-btn" @click="submitComment">发送</view>
		</view>
	</view>
</template>

<script>
	import { request } from '../../utils/request.js'
	import { fullUrl, formatTime } from '../../utils/config.js'

	export default {
		data() {
			return {
				id: null,
				project: null,
				comments: [],
				commentText: ''
			}
		},
		onLoad(options) {
			this.id = options.id
			this.loadDetail()
			this.loadComments()
		},
		methods: {
			fullUrl,
			formatTime,
			async loadDetail() {
				try {
					this.project = await request({ url: '/api/projects/' + this.id })
				} catch (e) {}
			},
			async loadComments() {
				try {
					const data = await request({ url: '/api/projects/' + this.id + '/comments' })
					this.comments = data.list
				} catch (e) {}
			},
			async submitComment() {
				const content = this.commentText.trim()
				if (!content) {
					uni.showToast({ title: '评论不能为空', icon: 'none' })
					return
				}
				try {
					await request({
						url: '/api/projects/' + this.id + '/comments',
						method: 'POST',
						data: { content }
					})
					this.commentText = ''
					this.loadComments()
					uni.showToast({ title: '评论成功', icon: 'success' })
				} catch (e) {}
			},
			preview(index) {
				const urls = this.project.images.map((i) => fullUrl(i))
				uni.previewImage({ current: urls[index], urls })
			}
		}
	}
</script>

<style scoped>
	.cover {
		width: 100%;
		height: 400rpx;
		border-radius: 16rpx;
		margin-bottom: 20rpx;
	}
	.title {
		font-size: 36rpx;
		font-weight: bold;
		display: block;
	}
	.meta {
		display: flex;
		justify-content: space-between;
		margin-top: 16rpx;
		font-size: 24rpx;
		color: #999;
	}
	.summary {
		font-size: 28rpx;
		color: #555;
		line-height: 1.6;
	}
	.detail {
		font-size: 28rpx;
		color: #555;
		line-height: 1.7;
		white-space: pre-wrap;
	}
	.imgs {
		display: flex;
		flex-wrap: wrap;
	}
	.img {
		width: 200rpx;
		height: 200rpx;
		margin: 0 16rpx 16rpx 0;
		border-radius: 12rpx;
	}
	.comment {
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}
	.comment:last-child {
		border-bottom: none;
	}
	.c-head {
		display: flex;
		justify-content: space-between;
		margin-bottom: 8rpx;
	}
	.c-name {
		font-size: 28rpx;
		font-weight: bold;
	}
	.c-time {
		font-size: 22rpx;
		color: #aaa;
	}
	.c-content {
		font-size: 28rpx;
		color: #444;
	}
	.empty {
		text-align: center;
		color: #999;
		padding: 30rpx 0;
	}
	.comment-bar {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		align-items: center;
		padding: 16rpx 20rpx;
		background: #fff;
		box-shadow: 0 -2rpx 8rpx rgba(0, 0, 0, 0.05);
	}
	.c-input {
		flex: 1;
		height: 64rpx;
		background: #f2f3f5;
		border-radius: 32rpx;
		padding: 0 24rpx;
		font-size: 28rpx;
	}
	.c-btn {
		margin-left: 20rpx;
		background: #3B82F6;
		color: #fff;
		padding: 12rpx 32rpx;
		border-radius: 32rpx;
		font-size: 28rpx;
	}
	.page {
		padding-bottom: 140rpx;
	}
</style>
