const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
// console.log(csrf)

const alertBox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

Dropzone.autoDiscover = false
// const myDropzone = new Dropzone('#my-dropzone', {
//     // url:'/upload/',
//     url:'upload/',
//     init: function() {
//         this.on('sending', function(file, xhr, formData) {
//             console.log('sending')
//             formData.append('csrfmiddlewaretoken', csrf)
//         })
//     },
//     maxFiles: 3,
//     maxFilesize: 3, // (i.e. 3MB)
//     acceptedFiles: '.csv'
// })
const myDropzone = new Dropzone('#my-dropzone', {
    // url:'/upload/',
    url:'/sales/from_file/upload/',
    init: function() {
        this.on('sending', function(file, xhr, formData) {
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response) {
            console.log(response)
            console.log(response.ex)
            const ex = response.ex
            if (ex) {
//                 alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
//   Error! File is already existing. Please try again.
// </div>`
                handleAlerts('danger', 'Error! File already exists. Please try again.')
            } else {
//                 alertBox.innerHTML = `<div class="alert alert-success" role="alert">
//   Success! Sales data has been uploaded.
// </div>`
                handleAlerts('success', 'Success! File has been successfully uploaded.')
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3, // (i.e. 3MB)
    acceptedFiles: '.csv'
})