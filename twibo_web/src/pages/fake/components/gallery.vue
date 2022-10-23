<template>
  <div class="gallery">
    <div class="carousel">
      <el-carousel
        trigger="click"
        :autoplay="false"
        height="600px"
        indicator-position="outside"
      >
        <el-carousel-item
          v-for="pic in picList"
          :key="pic.name"
          :name="pic.name"
          class="photo"
          ref="carou"
        >
          <el-card>
            <div v-if="pic.name === 'cheat'" class="day">
              <div class="poem">
                <div
                  v-for="(s, index) in silverKiller"
                  :key="index"
                  class="sentence"
                >
                  {{ s }}
                </div>
              </div>
              <el-input
                size="mini"
                v-model="cheatCode"
                placeholder=""
                @change="check"
                style="width: 200px"
              ></el-input>
            </div>
            <div v-else-if="pic.name === 'calendar'" class="day">
              <el-image
                src="/images/owl.png"
                style="width: 300; height: 300px; margin-bottom: 30px"
              ></el-image>
              <el-date-picker
                v-model="day"
                type="date"
                @change="checkDay"
              ></el-date-picker>
            </div>
            <el-image
              v-else
              fit="scale-down"
              :src="pic.url"
              style="width: 900px; height: 500px"
            ></el-image>
          </el-card>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>
<script>
export default {
  name: "gallery",
  data() {
    return {
      cheatCode: "",
      day: "",
      picList: [
        { name: "0", url: "/images/0.jpg" },
        { name: "1", url: "/images/1.jpg" },
        { name: "2", url: "/images/2.jpg" },
        { name: "3", url: "/images/3.jpg" },
        { name: "4", url: "/images/4.jpg" },
        { name: "5", url: "/images/5.jpg" },
        { name: "6", url: "/images/6.jpg" },
        { name: "7", url: "/images/7.jpg" },
        { name: "8", url: "/images/8.jpg" },
        { name: "9", url: "/images/9.jpg" },
        { name: "10", url: "/images/10.jpg" },
        { name: "11", url: "/images/11.jpg" },
        { name: "12", url: "/images/12.jpg" },
        { name: "calendar" },
      ],
      silverKiller: [
        "I've seen things you people wouldn't believe",
        "Attack ships on fire off the shoulder of Orion",
        "I watched C-beams glitter in the dark near the Tannhouser Gate",
        "... ",
        "All those moments will be lost in time",
        "Like tears",
        "In rain",
      ],
    };
  },
  methods: {
    checkDay() {
      if (!this.day) {
        return;
      }
      const year = this.day.getFullYear();
      const month = this.day.getMonth() + 1;
      const day = this.day.getDate();

      if (year === 1989 && month === 6 && day === 4) {
        this.$message({
          message: "这一天发生了什么？",
          type: "warning",
        });
      } else if (year === 1993 && month === 3 && day === 23) {
        this.$message({
          message: "你怎么记得我生日的？",
          type: "success",
        });
      } else if (year === 1987 && month === 9 && day === 14) {
        this.picList.push({ name: "cheat" });
        this.$message({
          message:
            "Across the great wall we can reach every corner in the world.",
          type: "warning",
          duration: 0,
          showClose: true,
        });
      } else {
        this.$message({
          message: "这一天对你一定很特别吧？",
          type: "success",
        });
      }
    },
    check() {
      if (this.cheatCode === "iseedeadpeople") {
        this.$emit("showJump");
      } else if (this.cheatCode === "greedisgood") {
        this.$emit(
          "showTrick",
          "Sun Tzu said: All warfare is based on deception"
        );
      } else if (this.cheatCode === "thereisnospoon") {
        this.$emit("showTrick", "Wake up, Neo");
      } else if (this.cheatCode === "whosyourdaddy") {
        this.$notify({
          message: "You talking to me?",
          type: "success",
        });
        this.$notify({
          message: "You talking to me?",
          type: "success",
          position: "bottom-right",
        });
        this.$notify({
          message: "You talking to me?",
          type: "success",
          position: "bottom-left",
        });
      } else {
        this.$emit("showTrick", "Less is More");
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.gallery {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.carousel {
  width: 80%;
  border: 1px 1px;
}
.photo {
  display: flex;
  justify-content: center;
  align-items: center;
}
.day {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.poem {
  margin-bottom: 30px;
  .sentence {
    font-size: 20px;
    padding: 10px;
    color: #043745;
  }
}
</style>
