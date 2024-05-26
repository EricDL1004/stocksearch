// 定義一個變數確定是否為編輯模式
var isInEditMode = false; 

// 取得HTML id
var groupContainer = document.getElementById('group-container');
var addButton = document.getElementById('add-button');
var editButton = document.getElementById('edit-button');
var modifyButton = document.getElementById('modify-button');
var deleteButton = document.getElementById('delete-button');
var deleteStocksButton = document.querySelectorAll('.delete-stock');
var change = document.querySelectorAll('#change');
// var settingsicon = document.getElementById('settings-icon');

// 隱藏新增、修改、刪除按鈕
addButton.style.display = "none";
modifyButton.style.display = "none";
deleteButton.style.display = "none";

// 編輯鈕監聽
editButton.addEventListener('click', function() { 
    // 切換為編輯模式
    isInEditMode = !isInEditMode; 

    // 如果處於編輯模式，則顯示新增、修改與刪除按鈕
    if (isInEditMode) {
        addButton.style.display = "block";
        modifyButton.style.display = "block";
        deleteButton.style.display = "block";
    } 
    // 非編輯模式，則隱藏按鈕
    else {
        addButton.style.display = "none";
        modifyButton.style.display = "none";
        deleteButton.style.display = "none";
    }
    if (this.innerHTML == "編輯") {
        this.innerHTML = "取消";
    } else {
        this.innerHTML = "編輯";
    }
    
    // // forEach 來走訪按鈕
    // deleteStocksButton.forEach(function (button) {
    //     // 檢查每個按鈕的 'display'屬性是否為 'none'
    //     if (button.style.display === 'none') {
    //         button.style.display = 'inline';
    //     } else {
    //         button.style.display = 'none';
    //     }
    // });
});

// 修改鈕監聽
modifyButton.addEventListener("click", function() { 
    // 若不處於編輯模式，則返回並不進行任何操作
    if (!isInEditMode) return; 

    // 取得所有群組按鈕
    var groupButtons = groupContainer.querySelectorAll('button.group');

    // 選擇要修改的群組的訊息
    var message = "請選擇要修改的群組：\n";
    groupButtons.forEach(function(btn, index) {
        message += (index + 1) + ". " + btn.textContent + "\n";
    });

    // 請求使用者輸入要修改的群組編號
    var groupNumber = prompt(message);

    // 如果輸入值不是數字或超出範圍，則取消操作
    if (!groupNumber || isNaN(groupNumber) || groupNumber < 1 || groupNumber > groupButtons.length) {
        alert('取消修改或無效的群組編號');
        return;
    }

    // 讓使用者輸入新的群組名稱
    var newGroupName = prompt("請輸入新的群組名稱：");
    if (newGroupName) {
        var groupToModify = groupButtons[groupNumber - 1];
        // 修改群組按鈕的文字
        groupToModify.textContent = newGroupName; 
        // 更新群組的ID屬性
        groupToModify.setAttribute('data-group-id', newGroupName.replace(/\s+/g, '')); 
    } else {
        alert('群組名稱不能為空');
    }    
});

// 刪除鈕監聽
deleteButton.addEventListener('click', function() {
    // 若不處於編輯模式，則返回並不進行任何操作
    if (!isInEditMode) return; 
    
    // 取得所有群組按鈕
    var groupButtons = groupContainer.querySelectorAll('button.group');
     
    // 如果只有一個群組按鈕，則返回並提示無法刪除
    if (groupButtons.length === 1) {
        alert("無法刪除唯一的群組");
        return;
    }

    // 提示使用者選擇要刪除的群組
    var message = "請選擇要刪除的群組：\n";
    groupButtons.forEach(function(btn, index) {
        message += (index + 1) + ". " + btn.textContent + "\n";
    });

    // 提示使用者輸入要刪除的群組編號
    var groupNumber = prompt(message);

    // 如果輸入值不是數字或超出範圍，則取消操作
    if (!groupNumber || isNaN(groupNumber) || groupNumber < 1 || groupNumber > groupButtons.length) {
        alert('取消刪除或無效的群組編號');
        return;
    }

    // 移除選擇的群組
    var groupToDelete = groupButtons[groupNumber - 1];
    if(groupToDelete) {
        groupContainer.removeChild(groupToDelete);
    }

});
// 走訪每個刪除按鈕並設置監聽
deleteStocksButton.forEach((button) => {
    button.addEventListener('click', (e) => { 
        // 阻止瀏覽器的預設行為
        e.preventDefault();
        var userConfirmed = confirm('確定要刪除股票代碼嗎？');
        if (userConfirmed) {
            document.getElementById('delete-form-' + button.getAttribute('data-stock-id')).submit();
        }
        
    });
});

// 新增鈕監聽        
addButton.addEventListener('click', function() {
    // 若不處於編輯模式，則返回並不進行任何操作
    if (!isInEditMode) return;

    // 取得所有群組按鈕
    var groupButtons = groupContainer.querySelectorAll('button.group'); 

    if (groupButtons.length < 5) {
        // 限制群組名稱長度，並創建新的群組按鈕
        var groupName = prompt("請輸入群組名稱，最多5個字");

        if (groupName === null || groupName === "") {
            alert('已取消建立自選股群組');
            return;
        }
        // 提示使用者群組名稱不超過5個字
        if (groupName.length > 5) {
            alert('群組名稱不能超過5個字');
            return;
        }

        // button元素
        var newButton = document.createElement('button');
        newButton.className = "group"; 
        // 設定 button 文字為群組名稱
        newButton.textContent = groupName; 

        // newButton.setAttribute('draggable', 'true');
        // newButton.id = "group-" + Date.now();

        newButton.setAttribute('data-group-id', groupName.replace(/\s+/g, ''));

        newButton.ondragstart = function(event) {
            drag(event);
        };
        // 新增 button到groupContainer中
        groupContainer.appendChild(newButton);          
    } else {
        // 若已達到群組數量限制，則顯示警告
        alert("已達到群組個數限制");
    }
});

// // 為每個按鈕添加點擊監聽事件
// document.querySelectorAll('.analysis-group button').forEach(button => {
//     button.addEventListener('click', () => {
//         // 獲取被點擊的按鈕文字
//         let buttonText = button.textContent;
        
//         // 根據按鈕文字決定新的表頭內容
//         let newHeader;

//         switch (buttonText) {
//             case '概覽':
//                 newHeader = `
//                 <tr>
//                     <th>成交價</th>
//                     <th>漲幅</th>
//                     <th>開盤價</th>
//                     <th>最高價</th>
//                     <th>最低價</th>
//                     <th>收盤價</th>
//                     <th>成交量</th>
//                     <th>123</th>
//                     <th>功能</th>
//                 </tr>
//                 `;
//                 break;

//             case '技術':
//                 newHeader = `
//                 <tr>
//                     <th>成交價</th>
//                     <th>漲幅</th>
//                     <th>開盤價</th>
//                     <th>最高價</th>
//                     <th>最低價</th>
//                     <th>收盤價</th>
//                     <th>成交量</th>
//                     <th>功能</th>
//                 </tr>
//                 `;
//             break;

//             case '法人':
//                 newHeader = `
//                 <tr>
//                     <th>成交價</th>
//                     <th>漲幅</th>
//                     <th>開盤價</th>
//                     <th>最高價</th>
//                     <th>最低價</th>
//                     <th>收盤價</th>
//                     <th>成交量</th>
//                     <th>外資買賣超(1日)</th>
//                     <th>外資買賣超(3日)</th>
//                     <th>外資買賣超(5日)</th>
//                     <th>投信買賣超(1日)</th>
//                     <th>投信買賣超(3日)</th>
//                     <th>投信買賣超(5日)</th>
//                     <th>功能</th>
//                 </tr>
//                 `;
//                 break;
//             case '主力':
//                 newHeader = `
//                 <tr>
//                     <th>成交價</th>
//                     <th>漲幅</th>
//                     <th>開盤價</th>
//                     <th>最高價</th>
//                     <th>最低價</th>
//                     <th>收盤價</th>
//                     <th>成交量</th>
//                     <th>功能</th>
//                 </tr>
//                 `;
//                 break;

//             case '基本':
//                 newHeader = `
//                 <tr>
//                     <th>成交價</th>
//                     <th>漲幅</th>
//                     <th>開盤價</th>
//                     <th>最高價</th>
//                     <th>最低價</th>
//                     <th>收盤價</th>
//                     <th>成交量</th>
//                     <th>功能</th>
//                 </tr>
//                 `;
//                 break;
//         }

//         // 更改表頭內容
//         document.querySelector('thead').innerHTML = newHeader;




        
//         // // 在此可以更改你的表頭內容
//         // document.querySelector('thead').innerHTML = `
//         //     <th>股票代碼</th>
//         //     <th>成交價</th>
//         //     <th>漲幅</th>
//         //     <th>開盤價</th>
//         //     <th>最高價</th>
//         //     <th>最低價</th>
//         //     <th>收盤價</th>
//         //     <th>成交量</th>
//         //     <th>外資買賣超(1日)</th>
//         //     <th>外資買賣超(3日)</th>`;
        
//     });
// });

change.forEach(function(changeElement) {
    var change = parseFloat(changeElement.innerText);
    if (change < 0){
        changeElement.style.color = 'green'
    }
    else if (change == 0){
        changeElement.style.color = 'gray'
    }
    else {
        changeElement.style.color = 'red'
    }
});



// document.addEventListener('DOMContentLoaded', function() {
//     var buttons = document.querySelectorAll('.analysis-group button');
//     buttons.forEach(function(button) {
//         button.addEventListener('click', function() {
//             var category = button.innerText; // 获取按钮文本（例如“技术”）
//             updateTable(category); // 调用更新表格的函数
//         });
//     });
// });

// function updateTable(category) {
//     fetch(`/update_table?category=${category}`) // 向服务器发送请求
//     .then(response => response.json())
//     .then(data => {
//         // 这里我们假设服务器返回的数据是直接可用于表格的HTML。
//         document.querySelector('thead').innerHTML = data['thead'];
//         document.querySelector('tbody').innerHTML = data['tbody'];
//     })
//     .catch(error => console.error('Error:', error));
// }