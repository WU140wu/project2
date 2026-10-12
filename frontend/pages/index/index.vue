<template>
	<view class="page">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<input class="search-input" v-model="keyword" placeholder="搜索项目标题" confirm-type="search" @confirm="onSearch" />
			<view class="search-btn" @click="onSearch">搜索</view>
		</view>

		<!-- 项目列表 -->
		<view v-if="list.length">
			<view class="card" v-for="item in list" :key="item.id" @click="goDetail(item.id)">
				<view class="cover-box">
					<image v-if="item.cover_url" class="cover" :src="fullUrl(item.cover_url)" mode="aspectFill"></image>
					<view v-else class="cover placeholder">暂无封面</view>
				</view>
				<view class="info">
					<text class="title">{{ item.title }}</text>
					<text class="summary">{{ item.summary }}</text>
					<view class="meta">
						<text class="author">{{ item.author ? item.author.nickname : '匿名' }}</text>
						<text class="count">{{ item.comment_count }} 评论</text>
					</view>
				</view>
			</view>
			<view class="load-state">
				<text>{{ finished ? '— 没有更多了 —' : '加载中…' }}</text>
			</view>
		</view>

		<!-- 空状态 -->
		<view v-else class="empty">
			<text>{{ loading ? '加载中…' : '还没有项目，去「发布」一个吧' }}</text>
		</view>
	</view>
</template>

<script>
	import { request } from '../../utils/request.js'
	import { fullUrl } from '../../utils/config.js'

	export default {
		data() {
			return {
				keyword: '',
				list: [],
				page: 1,
				pageSize: 10,
				total: 0,
				loading: false,
				finished: false
			}
		},
		onShow() {
			this.loadList(true)
		},
		onPullDownRefresh() {
			this.loadList(true, () => uni.stopPullDownRefresh())
		},
		onReachBottom() {
			this.loadList(false)
		},
		methods: {
			fullUrl,
			async loadList(reset, cb) {
				if (this.loading) return
				if (!reset && this.finished) return
				this.loading = true
				const page = reset ? 1 : this.page + 1
				try {
					const data = await request({
						url: '/api/projects',
						data: { page, page_size: this.pageSize, keyword: this.keyword }
					})
					this.list = reset ? data.list : this.list.concat(data.list)
					this.total = data.total
					this.page = page
					this.finished = this.list.length >= this.total
				} catch (e) {}
				this.loading = false
				cb && cb()
			},
			onSearch() {
				this.loadList(true)
			},
			goDetail(id) {
				uni.navigateTo({ url: '/pages/detail/detail?id=' + id })
			}
		}
	}
</script>

<style scoped>
	.search-bar {
		display: flex;
		align-items: center;
		background: #fff;
		border-radius: 12rpx;
		padding: 12rpx 16rpx;
		margin-bottom: 20rpx;
	}
	.search-input {
		flex: 1;
		height: 60rpx;
		font-size: 28rpx;
	}
	.search-btn {
		color: #3B82F6;
		font-size: 28rpx;
		padding: 0 16rpx;
	}
	.card {
		display: flex;
	}
	.cover-box {
		width: 200rpx;
		height: 150rpx;
		margin-right: 20rpx;
		flex-shrink: 0;
	}
	.cover {
		width: 200rpx;
		height: 150rpx;
		border-radius: 12rpx;
	}
	.cover.placeholder {
		background: #e5e7eb;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #9ca3af;
		font-size: 24rpx;
	}
	.info {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		overflow: hidden;
	}
	.title {
		font-size: 30rpx;
		font-weight: bold;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.summary {
		font-size: 26rpx;
		color: #666;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2;
		overflow: hidden;
	}
	.meta {
		display: flex;
		justify-content: space-between;
		font-size: 24rpx;
		color: #999;
	}
	.load-state {
		text-align: center;
		color: #999;
		font-size: 24rpx;
		padding: 10rpx 0 20rpx;
	}
	.empty {
		text-align: center;
		color: #999;
		padding-top: 200rpx;
	}
</style>
