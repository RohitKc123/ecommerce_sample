// const updateBtns = document.getElementsByClassName('update-cart');
//
// for(let i = 0; i< updateBtns.length; i++){
//     updateBtns[i].addEventListener('click', function(){
//         let productId = this.dataset.product
//         let action = this.dataset.action
//         console.log('productId:', productId, 'action:', action)
//
//         updateUserOrder(productId, action)
//     })
// }
//
// function updateUserOrder(productId, action){
//     let url = '/wish_list/'
//     fetch (url, {
//         method: 'POST',
//         headers:{
//             'content-type':'application/json'
//         },
//         body:JSON.stringify({'prodictId': productId, 'action' : action})
//     })
//         .then((response)=>{
//             return response.json()
//     })
//         .then((data)=>{
//             console.log('data',data)
//     })
// }
// // updateBtns[0].addEventListener('click', ()=>{
//     console.log("Helloworld")
// })


// console.log(updateBtns, 'length--> ', updateBtns.length)