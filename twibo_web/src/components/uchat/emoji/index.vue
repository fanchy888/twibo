<template>
  <el-popover placement="top" trigger="click">
    <el-tabs>
      <el-tab-pane
        v-for="category in categories"
        :key="`category_${category}`"
        :label="category"
      >
        <div class="emoji_picker">
          <div class="category">
            <button
              @click="handleEmojiClick($event, emoji)"
              v-for="(emoji, index) in category_emojis(category)"
              :key="`emoji_${index}`"
            >
              {{ emoji }}
            </button>
          </div>
        </div></el-tab-pane
      >
    </el-tabs>

    <span slot="reference" class="emoji-btn">😃</span>
  </el-popover>
</template>
<script>
import data from "./emojis-data.json";
export default {
  name: "emoji",
  props: {
    show_arrow: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  computed: {
    categories() {
      return Object.keys(data);
    },
    category_emojis: () => (category) => {
      return Object.values(data[category]);
    },
  },
  methods: {
    handleEmojiClick(e, emoji) {
      e.preventDefault();
      this.$emit("emoji_click", emoji);
    },
  },
};
</script>

<style scoped lang="scss">
.emoji_picker {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 25rem;
  height: 15rem;
  max-width: 100%;

  overflow: auto;
  z-index: 1;
}

.category button {
  margin: 0.5rem;
  margin-left: 0;
  background: inherit;
  border: none;
  font-size: 1rem;
  padding: 0;
}
.emoji-btn {
  padding-right: 2px;
}
.emoji-btn:hover {
  cursor: pointer;
}
</style>
