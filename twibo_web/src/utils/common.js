export const host = {
  localhost: "http://192.168.5.2:5000/",
  production: "http://www.twibo.icu/",
};

export const staticUrl = host.production + "static/";
export const timedelta = new Date().getTimezoneOffset() * 60 * 1000;

export function avatarSrc(avatar) {
  return staticUrl + avatar;
}

export function convertTime(t) {
  if (!t) return "";
  const time = new Date(t * 1000 - timedelta);
  const year = time.getFullYear();
  const month = time.getMonth() + 1;
  const day = time.getDate();
  const hour = time.getHours();
  let minite = time.getMinutes();
  if (minite < 10) {
    minite = "0" + minite;
  }
  return year + "-" + month + "-" + day + " " + hour + ":" + minite;
}
