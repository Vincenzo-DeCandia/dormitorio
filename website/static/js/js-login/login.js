
let cod_fisc = document.getElementById('cod_fisc');
let password = document.getElementById('password');
let submit = document.getElementById('submit_button');

/*
submit.addEventListener('click', (event) => {
    postJSON();
})


async function postJSON(){
    let entry = {
        user: cod_fisc.value,
        passw: password.value
    }

    await fetch('/validate-login', {
        method: 'POST',
        credentials: 'include',
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json',
        }),
        body: JSON.stringify(entry),
    }).then((res) => {
        if (res.status === 200) {
            console.log('200');
        }
        else {
            console.log('Error');
        }
    })
}
*/

