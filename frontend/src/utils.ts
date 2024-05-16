export function triageToColor(triage?: string): string {
    let color = 'gray'
    switch (triage) {
        case 'X':
            color = 'black'
            break
        case '1':
            color = 'red'
            break
        case '2':
            color = 'yellow'
            break
        case '3':
            color = 'green'
            break
    }
    return "var(--" + color + ")"
}