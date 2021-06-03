// console.log('Hello World')

const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')

const reportForm = document.getElementById('report-form')

const alertBox = document.getElementById('alert-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
// console.log(csrf)
const reportName = document.getElementById('id_name')
// console.log(reportName)
const reportRemarks = document.getElementById('id_remarks')
// console.log(reportRemarks)

// console.log(reportBtn)
// console.log(img)

if (img) {
    reportBtn.classList.remove('not-visible')
}

reportBtn.addEventListener('click', ()=>{
    // console.log('clicked')
    // modalBody.append(img)
    img.setAttribute('class', 'w-100')
    modalBody.prepend(img)

    console.log(img.src)

    reportForm.addEventListener('submit', e=>{
        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({
            type: 'POST',
            // url: '/reports/save/',
            // url: '/reports/savee/',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                console.log(response)
                handleAlerts('success', 'Report successfully created')
                reportForm.reset()
            },
            error: function(error){
                console.log(error)
                handleAlerts('danger', 'Error! Something went wrong')
            },
            processData: false,
            contentType: false
        })
    })
})

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}