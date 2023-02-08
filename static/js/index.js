const header_elm = document.getElementById('header');
const imageEle = document.getElementById('img-preview');
const form_elm = document.getElementById('file-upload-form');
const submit_btn = document.getElementById('submit-button');
const input_img_elm = document.getElementById('uploadFile');
// const paste_img_btn = document.getElementById('paste-button')

const hide_header = () => {
    header_elm.style.display = 'none';

}

// Drag and Drop js code
function drag() {
    document.getElementById('uploadFile').parentNode.className = 'draging dragBox';
}
function drop() {
    document.getElementById('uploadFile').parentNode.className = 'dragBox';
}
function dragNdrop(event) {
    let fileType = event.target.files[0].type
    if ( !((fileType==='image/png') ||  (fileType==='image/jpg') || (fileType==='image/jpeg') )) {
        alert('Selected file is not an image');
        return 
    }
    let fileName = URL.createObjectURL(event.target.files[0]);
    imageEle.setAttribute("src", fileName);
    imageEle.setAttribute("width", '100%');
    hide_header();
}


// Paste (ctr+v) js code 
document.addEventListener('paste', evt => {

    const clipboardItems = evt.clipboardData.items;
    const items = [].slice.call(clipboardItems).filter(function (item) {
        // Filter the image items only
        return item.type.indexOf('image') !== -1;
    });
    if (items.length === 0) {
        let msg = 'Copied item is not an image';
        alert(msg);
        return;
    }
    input_img_elm.files = evt.clipboardData.files

    const item = items[0];
    // Get the blob of image
    const blob = item.getAsFile();
    const fileName = URL.createObjectURL(blob);
    imageEle.setAttribute("src", fileName);
    imageEle.setAttribute("width", '100%');
    hide_header();
});

// paste_img_btn.addEventListener('click', () => {
//     console.log('Paste btn is clicked')
//     const clipboardItems = evt.clipboardData.items;
//     const items = [].slice.call(clipboardItems).filter(function (item) {
//         // Filter the image items only
//         return item.type.indexOf('image') !== -1;
//     });
//     if (items.length === 0) {
//         let msg = 'Copied item is not an image';
//         alert(msg);
//         return;
//     }
//     input_img_elm.files = evt.clipboardData.files

//     const item = items[0];
//     // Get the blob of image
//     const blob = item.getAsFile();
//     const fileName = URL.createObjectURL(blob);
//     imageEle.setAttribute("src", fileName);
//     imageEle.setAttribute("width", '100%');
//     hide_header();
// }

// )



document.addEventListener("keydown", (e)=> {
    if (e.key==='Enter')
    {
        e.preventDefault();
        submit_btn.click();
    }

});
