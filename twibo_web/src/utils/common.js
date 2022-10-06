export const staticUrl = "http://101.42.236.38/static/";
export const timedelta = new Date().getTimezoneOffset() * 60 * 1000;

export function avatarSrc(avatar) {
  return staticUrl + avatar;
}
