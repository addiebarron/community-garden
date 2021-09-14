// https://github.com/sveltejs/kit/tree/master/packages/adapter-static
import adapter from "@sveltejs/adapter-static";

export default {
  kit: {
    adapter: adapter({
      // default options are shown
      pages: "build",
      assets: "build",
      fallback: null,
    }),
  },
  ssr: false,
};
