function togglePw() {
    const input = document.getElementById('password')
    const icon  = document.getElementById('pw-icon')

    if (input.type === 'password') {
        input.type      = 'text'
        icon.className  = 'bi bi-eye-slash'
    } else {
        input.type      = 'password'
        icon.className  = 'bi bi-eye'
    }
}