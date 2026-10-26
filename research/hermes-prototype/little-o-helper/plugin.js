import { KEYBINDS_AREA } from '@hermes/plugin-sdk'

const VOICE_TOGGLE_EVENT = 'hermes:composer-voice-toggle'

function toggleMainVoiceConversation() {
  window.dispatchEvent(
    new CustomEvent(VOICE_TOGGLE_EVENT, {
      detail: { target: 'main' }
    })
  )
}

export default {
  id: 'little-o-helper',
  name: 'Little O Helper Bridge',
  register(ctx) {
    ctx.register({
      id: 'toggle-voice',
      area: KEYBINDS_AREA,
      data: {
        id: 'little-o.helper.toggleVoice',
        category: 'composer',
        defaults: ['ctrl+alt+b'],
        label: 'Little O: Start or stop voice conversation',
        run: toggleMainVoiceConversation
      }
    })
  }
}
