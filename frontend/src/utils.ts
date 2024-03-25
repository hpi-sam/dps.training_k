export function triageToColor(triage?: string): string {
    let color = 'gray'
    switch (triage) {
        case 'R':
        case 'A':
        case 'B':
        case 'C':
        case 'D':
        case 'E':
            color = 'red'
            break
        case 'Y':
            color = 'yellow'
            break
        case 'G':
            color = 'green'
            break
    }
    return "var(--" + color + ")"
}