<script>
</script>

<div class="container">
	<div class="ball ball1"></div>
	<div class="ball ball2"></div>
	<div class="ball ball3"></div>
</div>

<style>
	.container {
		padding: 5px 10px 10px 10px;

		display: flewx;
		width: 40px;
		justify-content: space-between;
		height: 20px;
		align-items: flex-end;
	}
	.ball {
		width: 10px;
		height: 10px;
		background: #333;
		border-radius: 50%;
		animation: bounce 1.2s inifinte ease-in-out;
	}

	.ball1 {
	}

	.ball2 {
		animation-delay: 0.2s;
	}

	.ball3 {
		animation-delay: 0.4s;
	}

	@keyframes bounc {
		0% {
			transform: translate(0, 0);
		}
		25% {
			transform: translate(0, -10px);
			background: #ccc;
		}
		40% {
			transform: translate(0, px);
		}
		50% {
			transform: translate(0, 0px);
		}
	}
</style>
