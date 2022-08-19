async function download(data) {
    const blob = new Blob([data], { type: 'application/vnd.ms-excel' })
    const FILE = window.URL.createObjectURL(blob);
    const fileLink = document.createElement('a')
    
    const reader = new FileReader();
    reader.readAsDataURL(blob)
    console.log(reader.result);

    fileLink.href = FILE;
    fileLink.setAttribute('download', 'inventory_read_result.xls');
    document.body.appendChild(fileLink);

    fileLink.click();
}

export { download };