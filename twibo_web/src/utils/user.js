export function currentUser() {
  return JSON.parse(sessionStorage.getItem("userInfo"));
}
