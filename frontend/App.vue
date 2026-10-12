<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/* 全局公共样式 */
	page {
		background-color: #F5F6F8;
		font-size: 28rpx;
		color: #333;
	}

	.page {
		padding: 20rpx;
		box-sizing: border-box;
	}

	.card {
		background: #fff;
		border-radius: 16rpx;
		margin-bottom: 20rpx;
		padding: 20rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
	}

	.section-title {
		font-size: 30rpx;
		font-weight: bold;
		margin: 24rpx 0 12rpx;
		display: block;
	}

	.btn-primary {
		background: #3B82F6;
		color: #fff;
		border-radius: 12rpx;
		font-size: 30rpx;
	}
</style>
