function t(url, event_id){
    let event = event_id || ''
    let uuid = ''
    if(localStorage.getItem('uuid') !== 'undefined' && localStorage.getItem('uuid') !== null){
        uuid = localStorage.getItem('uuid')
    }
    console.log()
    let data = {
        'uuid': uuid,
        'ip': 'ip',
        'event_id': event,
        'url':location.href
    }
    // console.log(data)
    fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body:JSON.stringify(data)

        }
    )
    .then((response) => response.json())
    .then((response)=>{
        //if uuid is returned then store it
        localStorage.setItem('uuid', response.uuid);
    })
}