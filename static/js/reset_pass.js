function togglePw(fieldId, iconId) {
    const input = document.getElementById(fieldId)
    const icon  = document.getElementById(iconId)

    if (input.type === 'password') {
        input.type     = 'text'
        icon.className = 'bi bi-eye-slash'
    } else {
        input.type     = 'password'
        icon.className = 'bi bi-eye'
    }
}

// Valida se as senhas coincidem antes de submeter
document.querySelector('form').addEventListener('submit', function (e) {
    const pw      = document.getElementById('password').value
    const confirm = document.getElementById('confirm_password').value
    const error   = document.getElementById('match-error')
    const btn     = document.getElementById('btn-submit')

    if (pw !== confirm) {
        e.preventDefault()
        error.style.display = 'block'
        btn.style.background = '#e5e7eb'
        btn.style.color      = '#9ca3af'
        btn.style.cursor     = 'not-allowed'
    }
})

// Esconde o erro enquanto o usuário digita
document.getElementById('confirm_password').addEventListener('input', function () {
    document.getElementById('match-error').style.display = 'none'
    const btn = document.getElementById('btn-submit')
    btn.style.background = ''
    btn.style.color      = ''
    btn.style.cursor     = ''
})