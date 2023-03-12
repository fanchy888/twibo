import api from "@/plugins/api";
import { imgSrc } from "../../../utils/common";
class MyUploadAdapter {
  constructor(loader) {
    // The file loader instance to use during the upload.
    this.loader = loader;
  }

  // Starts the upload process.
  async upload() {
    const data = new FormData();
    const file = await this.loader.file;
    data.append("file", file);
    const res = await api.uploadBlogImage({ $body: data });

    return { default: imgSrc(res.url) };
  }
}

export function MyCustomUploadAdapterPlugin(editor) {
  editor.plugins.get("FileRepository").createUploadAdapter = (loader) => {
    // Configure the URL to the upload script in your back-end here!
    return new MyUploadAdapter(loader);
  };
}
