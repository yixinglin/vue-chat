<template>
  <div class="home">
    <div class="iframe-container">
      <iframe src="//player.bilibili.com/player.html?aid=990229258&bvid=BV1Mx4y137fa&cid=963687235&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
    </div>
    <!-- <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>

<style>
.iframe-container {
  padding-top: 56.25%;
  position: relative;
}

.iframe-container iframe {
  position: absolute;
  text-align: center;
  margin: auto;
  height: 50%;
  width: 50%;
  top: 0;
  left: 0;
  right: 0;
}

</style>

