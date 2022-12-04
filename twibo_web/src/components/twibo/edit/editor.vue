<template>
  <div class="editor">
    <div v-html="editorData"></div>
    <ckeditor
      :editor="editor"
      v-model="editorData"
      :config="editorConfig"
    ></ckeditor>
  </div>
</template>
<script>
import Editor from "ckeditor5-custom-build/build/ckeditor";
export default {
  name: "TwiboEditor",
  components: {},
  data() {
    return {
      editor: Editor,
      editorData: "",
      editorConfig: {
        // The configuration of the editor.
      },
    };
  },
};
</script>
<style lang="scss" scoped>
.editor {
  height: 200px;
}
</style>
