// 選擇所有需要監聽的元素
var profileLink = document.getElementById('profileLink');
var profileMenu = document.getElementById('profileMenu');
var timer;

// 監聽SVG圖標的滑鼠進入事件
profileLink.addEventListener('mouseover', function() {
  // 顯示選單
  profileMenu.style.display = 'block';
});

// 監聽SVG圖標的滑鼠離開事件
// profileLink.addEventListener('mouseout', function() {
//   // 啟動計時器，在一段時間後隱藏選單
//   timer = setTimeout(function() {
//     profileMenu.style.display = 'none';
//   }, 3000); // 這裡的3000表示延遲時間為3秒，單位是毫秒（ms）
// });

// 監聽選單的滑鼠進入事件
profileMenu.addEventListener('mouseover', function() {
  // 清除計時器，避免選單在滑鼠移到選單上時被隱藏
  clearTimeout(timer);
  profileMenu.style.display = 'block';
}); 

// 監聽選單的滑鼠離開事件
profileMenu.addEventListener('mouseout', function() {
  // 啟動計時器，在一段時間後隱藏選單
  timer = setTimeout(function() {
    profileMenu.style.display = 'none';
  }, 3000); // 這裡的3000表示延遲時間為3秒，單位是毫秒（ms）
});
