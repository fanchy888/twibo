import axios from "./axios";
import { isEmpty, deepCopy } from "@/utils/object";

const defaultConfig = { showLoading: true };
const isProduction = process.env.NODE_ENV === "production";
export class MakeRequestService {
  constructor(options) {
    this.api = {};
    this.buildRequests(options);
  }

  buildRequests(opts) {
    const { config = [], mockBaseURL = "" } = opts;

    config.forEach((api) => {
      const {
        name = "",
        desc = "",
        params = {},
        method = "get",
        path = "",
        mock = false,
        mockPath = "",
        keep = false,
      } = api;

      Object.defineProperty(this.api, `${name}`, {
        value(outerParams = {}, outerOptions = {}) {
          const url = !isProduction && mock && mockPath ? mockPath : path;
          const options = Object.assign(
            {
              url,
              desc,
              method,
              baseURL: mockBaseURL,
              keep,
            },
            {
              ...outerOptions,
              ...defaultConfig,
            }
          );

          const reqData = isEmpty(outerParams)
            ? params
            : { ...params, ...outerParams };

          return axios(normoalize(options, reqData));
        },
      });
    });
  }
}

// RESTful compatible
function normoalize(options, data) {
  const method = options.method.toLowerCase();
  const _data = deepCopy(data);
  const opts = deepCopy(options);
  const { $query, $body } = _data;

  // build url
  const currentPath = opts.url
    .split("/")
    .map((val) => {
      // console.log(val);
      if (val.indexOf(":") === 0) {
        const key = val.slice(1);
        val = val.slice(1);
        if (val) {
          if (val in (opts || {})) {
            val = opts[val] || "";
            delete opts[key];
          } else if (val in _data) {
            val = data[val] || "";
            delete _data[key];
          } else {
            if (val in $body) {
              val = $body[val] || "";
              delete $body[key];
            } else {
              val = "";
            }
          }
        }
      }

      return val.toString();
    })
    .map((x) => x.trim())
    .map((x) => encodeURIComponent(x))
    .filter((y) => !!y)
    .join("/");

  opts.url = `/${currentPath}`;

  if (["post", "put", "patch"].includes(method)) {
    // query
    if ($query) {
      opts.params = $query;
      delete _data.$query;
    }
    // body
    if ($body) {
      opts.data = $body;
    } else {
      opts.data = _data;
    }
  } else if (["get", "head", "delete"].includes(method)) {
    if ($query) {
      opts.params = $query;
      delete _data.$query;
    } else {
      opts.params = _data;
    }
  }

  return opts;
}
const API_DEFAULT_CONFIG = {
  mockBaseURL: "",
  debug: false,
  download_v2API: false,
};

const r = require.context("@/api/", true, /\.js$/);

let apisConfig = [];

r.keys().forEach((key) => {
  const module = r(key);

  if (module.default && Array.isArray(module.default)) {
    apisConfig = apisConfig.concat(module.default);
  }
});
// exmaple: this.api -> {getUsers() {...}}
export default new MakeRequestService({
  config: apisConfig,
  ...API_DEFAULT_CONFIG,
})["api"];
