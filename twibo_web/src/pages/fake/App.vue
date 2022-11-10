<template>
  <div id="fake">
    <home></home>
    <div class="foot">
      <div style="width: 150px; padding: 20px 0">
        <a
          target="_blank"
          href="https://beian.miit.gov.cn"
          style="
            display: inline-block;
            text-decoration: none;
            height: 20px;
            line-height: 20px;
            font-size: 10px;
          "
        >
          <p
            style="
              float: left;
              height: 20px;
              line-height: 20px;
              margin: 0px 0px 0px 5px;
              color: #939393;
            "
          >
            蒙ICP备2022003460号-1
          </p></a
        >
      </div>
      <div style="width: 300px; padding: 20px 0">
        <a
          target="_blank"
          href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802040738"
          style="
            display: inline-block;
            text-decoration: none;
            height: 20px;
            line-height: 20px;
            font-size: 10px;
          "
          ><img src="beian.png" style="float: left" />
          <p
            style="
              float: left;
              height: 20px;
              line-height: 20px;
              margin: 0px 0px 0px 5px;
              color: #939393;
            "
          >
            京公网安备 11010802040738号
          </p></a
        >
      </div>
    </div>
  </div>
</template>
<script>
import home from "./components/home";
export default {
  components: { home },
};
</script>
<style lang="scss">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html,
body,
#fake {
  font-family: "PingFang SC";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
  width: 100%;
}
::-webkit-scrollbar {
  width: 2px;
}
::-webkit-scrollbar-thumb {
  background-color: #eaecf1;
  border-radius: 1px;
}

.foot {
  display: flex;
  justify-content: center;
}
</style>
