const LANG_KEY = 'inline_lang';

const I18N = {
    ru: {
        back: '\u2190 \u041d\u0430\u0437\u0430\u0434',
        backHome: '\u2190 \u041d\u0430 \u0433\u043b\u0430\u0432\u043d\u0443\u044e',
        savedQueues: '\u0412\u0430\u0448\u0438 \u043e\u0447\u0435\u0440\u0435\u0434\u0438',
        deletedQueues: '\u0423\u0434\u0430\u043b\u0451\u043d\u043d\u044b\u0435 \u043e\u0447\u0435\u0440\u0435\u0434\u0438',
        organizer: '\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0442\u043e\u0440',
        participant: '\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a',
        createQueue: '\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043e\u0447\u0435\u0440\u0435\u0434\u044c',
        createQueueDesc: '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u0442\u0435 \u0438 \u043f\u043e\u0434\u0435\u043b\u0438\u0442\u0435\u0441\u044c \u0441\u0441\u044b\u043b\u043a\u043e\u0439',
        joinQueue: '\u0412\u0441\u0442\u0443\u043f\u0438\u0442\u044c \u0432 \u043e\u0447\u0435\u0440\u0435\u0434\u044c',
        joinQueueDesc: '\u0412\u0432\u0435\u0434\u0438\u0442\u0435 4-\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u043a\u043e\u0434',
        enter: '\u0412\u043e\u0439\u0442\u0438',
        feature1Title: '\u0411\u044b\u0441\u0442\u0440\u043e',
        feature1Desc: '\u041e\u0447\u0435\u0440\u0435\u0434\u044c \u0437\u0430 10 \u0441\u0435\u043a\u0443\u043d\u0434',
        feature2Title: '\u041f\u0440\u043e\u0441\u0442\u043e',
        feature2Desc: '\u0411\u0435\u0437 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0439',
        feature3Title: '\u0423\u0434\u043e\u0431\u043d\u043e',
        feature3Desc: 'QR-\u043a\u043e\u0434 \u0438\u043b\u0438 4-\u0437\u043d\u0430\u0447\u043d\u044b\u0439 \u043a\u043e\u0434',
        or: '\u0438\u043b\u0438',

        createTitle: '\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043e\u0447\u0435\u0440\u0435\u0434\u044c',
        nameLabel: '\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 *',
        namePlaceholder: '\u042d\u043a\u0437\u0430\u043c\u0435\u043d, \u0437\u0430\u0441\u0435\u043b\u0435\u043d\u0438\u0435...',
        descLabel: '\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
        descPlaceholder: '\u041e\u043f\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e',
        maxPeople: '\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c \u043b\u044e\u0434\u0435\u0439',
        perSlot: '\u0427\u0435\u043b\u043e\u0432\u0435\u043a \u0432 \u0441\u043b\u043e\u0442\u0435',
        perSlotHint: '\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u043b\u044e\u0434\u0435\u0439 \u043d\u0430 \u043e\u0434\u043d\u043e \u0432\u0440\u0435\u043c\u044f',
        allowDelay: '\u0420\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u044c "\u0437\u0430\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u044e\u0441\u044c"',
        allowSwap: '\u0420\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u044c \u0441\u043c\u0435\u043d\u0443 \u0441\u043b\u043e\u0442\u0430/\u043c\u0435\u0441\u0442\u0430',
        useTimeSlots: '\u0421 \u0442\u0430\u0439\u043c-\u0441\u043b\u043e\u0442\u0430\u043c\u0438',
        slotsConfig: '\u0421\u043b\u043e\u0442\u044b',
        startTime: '\u041d\u0430\u0447\u0430\u043b\u043e',
        slotDuration: '\u0414\u043b\u0438\u0442. \u0441\u043b\u043e\u0442\u0430 (\u043c\u0438\u043d)',
        participantInfo: '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u0434\u043b\u044f \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u0432',
        infoPlaceholder: '\u0410\u0443\u0434\u0438\u0442\u043e\u0440\u0438\u044f 301, \u0432\u0437\u044f\u0442\u044c \u043f\u0430\u0441\u043f\u043e\u0440\u0442...',
        windowLabel: '\u041e\u043a\u043d\u043e \u0434\u043b\u044f \u043e\u043f\u043e\u0437\u0434\u0430\u0432\u0448\u0438\u0445 (\u043c\u0438\u043d)',
        latePolicy: '\u041e\u043f\u043e\u0437\u0434\u0430\u0432\u0448\u0438\u0435',
        toEnd: '\u0412 \u043a\u043e\u043d\u0435\u0446 \u043e\u0447\u0435\u0440\u0435\u0434\u0438',
        discard: '\u0423\u0434\u0430\u043b\u0438\u0442\u044c',
        create: '\u0421\u043e\u0437\u0440\u0430\u043d\u0438\u0442\u044c',

        joinTitle: 'Inline \u2014 \u0412\u0441\u0442\u0443\u043f',
        alreadyJoined: '\u0412\u044b \u0443\u0436\u0435 \u0432 \u043e\u0447\u0435\u0440\u0435\u0434\u0438',
        continue: '\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c',
        loginOther: '\u0412\u043e\u0439\u0442\u0438 \u043a\u0430\u043a \u0434\u0440\u0443\u0433\u043e\u0439',
        yourName: '\u0412\u0430\u0448\u0435 \u0438\u043c\u044f *',
        namePlaceholder2: '\u041a\u0430\u043a \u043a \u0432\u0430\u043c \u043e\u0431\u0440\u0430\u0449\u0430\u0442\u044c\u0441\u044f?',
        joinBtn: '\u0412\u0441\u0442\u0430\u0442\u044c \u0432 \u043e\u0447\u0435\u0440\u0435\u0434\u044c',
        max: '\u041c\u0430\u043a\u0441:',
        swapEnabled: '\u041e\u0431\u043c\u0435\u043d \u0432\u043a\u043b.',
        delayEnabled: '\u0417\u0430\u0434\u0435\u0440\u0436\u043a\u0438',

        queueCode: '\u041a\u043e\u0434 \u043e\u0447\u0435\u0440\u0435\u0434\u0438',
        clickToCopy: '\u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u0447\u0442\u043e\u0431\u044b \u0441\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c',
        copied: '\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u043e',
        copyError: '\u041e\u0448\u0438\u0431\u043a\u0430',
        copy: '\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c',
        saved: '\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u043e',

        pause: '\u041f\u0430\u0437\u0443\u0437\u0430',
        resume: '\u0412\u043e\u0437\u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c',
        reopen: '\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0437\u0430\u043d\u043e\u0432\u043e',
        close: '\u0417\u0430\u043a\u0440\u044b\u0442\u044c',
        callNext: '\u0412\u044b\u0437\u0432\u0430\u0442\u044c \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u0433\u043e',
        exportXlsx: '\u042d\u043a\u0441\u043f\u043e\u0440\u0442 XLSX',
        deleteQueue: '\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043e\u0447\u0435\u0440\u0435\u0434\u044c',
        settings: '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438',
        save: '\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c',
        slots: '\u0421\u043b\u043e\u0442\u044b',
        inQueue: '\u0432 \u043e\u0447\u0435\u0440\u0435\u0434\u0438',
        you: '\u0412\u044b',
        allParticipants: '\u0412\u0441\u0435 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u0438',
        noSlotParticipants: '\u041d\u0435\u0442 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u0432 \u0432 \u044d\u0442\u043e\u043c \u0441\u043b\u043e\u0442\u0435',
        served: '\u041e\u0431\u0441\u043b\u0443\u0436\u0435\u043d\u044b / \u041f\u0440\u043e\u043f\u0443\u0449\u0435\u043d\u044b',
        emptyQueue: '\u041e\u0447\u0435\u0440\u0435\u0434\u044c \u043f\u0443\u0441\u0442\u0430',
        called: '\u0412\u044b\u0437\u0432\u0430\u043d',
        delayed: '\u0417\u0430\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442\u0441\u044f',
        servedStatus: '\u041e\u0431\u0441\u043b\u0443\u0436\u0435\u043d',
        skipped: '\u041f\u0440\u043e\u043f\u0443\u0449\u0435\u043d',
        servedTitle: '\u041e\u0431\u0441\u043b\u0443\u0436\u0435\u043d',
        skipTitle: '\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c',
        undoTitle: '\u0412\u0435\u0440\u043d\u0443\u0442\u044c',
        undo: '\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c',
        selected: '\u0432\u044b\u0431\u0440\u0430\u043d\u043e',
        move: '\u041f\u0435\u0440\u0435\u043c\u0435\u0441\u0442\u0438\u0442\u044c',
        deselect: '\u0421\u043d\u044f\u0442\u044c',
        loading: '\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430...',

        swapRequests: '\u0417\u0430\u043f\u0440\u043e\u0441\u044b \u0438 \u043e\u0431\u043c\u0435\u043d',
        swapHint: '\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0439\u0442\u0435 \u0441\u043c\u0435\u043d\u0443 \u0441\u043b\u043e\u0442\u0430 \u0438\u043b\u0438 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \u0442\u043e\u043b\u044c\u043a\u043e \u043f\u0440\u0438 \u0443\u0432\u0430\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0439 \u043f\u0440\u0438\u0447\u0438\u043d\u0435. \u0427\u0430\u0441\u0442\u044b\u0435 \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u0441\u043e\u0437\u0434\u0430\u044e\u0442 \u043d\u0435\u0443\u0434\u043e\u0431\u0441\u0442\u0432\u0430 \u0434\u043b\u044f \u0434\u0440\u0443\u0433\u0438\u0445 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u0432 \u0438 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0442\u043e\u0440\u0430.',
        swapSlot: '\u0421\u043c\u0435\u043d\u0438\u0442\u044c \u0441\u043b\u043e\u0442',
        swapPosition: '\u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0432 \u0441\u043b\u043e\u0442\u0435',
        selectSwapUser: '\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u0430 \u0434\u043b\u044f \u043e\u0431\u043c\u0435\u043d\u0430 \u0441\u043b\u043e\u0442\u043e\u043c',
        selectPosUser: '\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u0430 \u0434\u043b\u044f \u043e\u0431\u043c\u0435\u043d\u0430 \u043f\u043e\u0437\u0438\u0446\u0438\u0435\u0439',
        sendRequest: '\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u043f\u0440\u043e\u0441',
        noParticipants: '\u041d\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0445 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u0432',
        noSlotParticipants2: '\u041d\u0435\u0442 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u0432 \u0432 \u0441\u043b\u043e\u0442\u0435',
        swapDone: '\u041e\u0431\u043c\u0435\u043d \u0441\u043e\u0432\u0435\u0440\u0448\u0451\u043d!',

        positionLabel: '\u0412\u0430\u0448\u0430 \u043f\u043e\u0437\u0438\u0446\u0438\u044f',
        positionInSlot: '\u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0432 \u0441\u043b\u043e\u0442\u0435:',
        yourSlot: '\u0412\u0430\u0448 \u0441\u043b\u043e\u0442',
        itsYourTurn: '\u0421\u0435\u0439\u0447\u0430\u0441 \u0432\u0430\u0448\u0430 \u043e\u0447\u0435\u0440\u0435\u0434\u044c!',
        youCalled: '\u0412\u044b\u0437\u0432\u0430\u043d',
        youServed: '\u0412\u044b \u043e\u0431\u0441\u043b\u0443\u0436\u0435\u043d\u044b',
        statusWaiting: '\u041e\u0436\u0438\u0434\u0430\u0435\u0442',
        delayedBtn: '\u0417\u0430\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u044e\u0441\u044c',
        leaveQueue: '\u041f\u043e\u043a\u0438\u043d\u0443\u0442\u044c \u043e\u0447\u0435\u0440\u0435\u0434\u044c',
        schedule: '\u0420\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
        emptyList: '\u041f\u043e\u043a\u0430 \u043d\u0438\u043a\u043e\u0433\u043e \u043d\u0435\u0442',
        inSlot: '\u0432 \u0441\u043b\u043e\u0442\u0435',

        incomingSwap: '\u0417\u0430\u043f\u0440\u043e\u0441 \u043d\u0430 \u0441\u043c\u0435\u043d\u0443',
        accept: '\u041f\u0440\u0438\u043d\u044f\u0442\u044c',
        reject: '\u041e\u0442\u043a\u043b\u043e\u043d\u0438\u0442\u044c',
        cancel: '\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c',
        yourRequest: '\u0412\u0430\u0448 \u0437\u0430\u043f\u0440\u043e\u0441:',
        confirmLeave: '\u041f\u043e\u043a\u0438\u043d\u0443\u0442\u044c \u043e\u0447\u0435\u0440\u0435\u0434\u044c? \u0412\u044b \u0431\u0443\u0434\u0435\u0442\u0435 \u0443\u0434\u0430\u043b\u0435\u043d\u044b \u0438\u0437 \u0441\u043f\u0438\u0441\u043a\u0430.',
        confirmClose: '\u0417\u0430\u043a\u0440\u044b\u0442\u044c \u043e\u0447\u0435\u0440\u0435\u0434\u044c?',
        confirmDelete: '\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043e\u0447\u0435\u0440\u0435\u0434\u044c \u043d\u0430\u0432\u0441\u0435\u0433\u0434\u0430? \u042d\u0442\u043e \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435 \u043d\u0435\u043e\u0431\u0440\u0430\u0442\u0438\u043c\u043e.',
        undoHint: '\u0427\u0435\u043b\u043e\u0432\u0435\u043a \u043e\u0431\u0441\u043b\u0443\u0436\u0435\u043d',
        undoSkip: '\u0427\u0435\u043b\u043e\u0432\u0435\u043a \u043f\u0440\u043e\u043f\u0443\u0449\u0435\u043d',
        slotFull: '\u0421\u043b\u043e\u0442 \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d',
        notFound: '\u041e\u0447\u0435\u0440\u0435\u0434\u044c \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u0430',
        error: '\u041e\u0448\u043b\u0438\u0431\u043a\u0430',
        newParticipant: '\u041d\u043e\u0432\u044b\u0439 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a:',
        personDelayed: ' \u0437\u0430\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442\u0441\u044f',
        newSwapRequest: '\u041d\u043e\u0432\u044b\u0439 \u0437\u0430\u043f\u0440\u043e\u0441 \u043d\u0430 \u0441\u043c\u0435\u043d\u0443',
        noRequests: '\u041d\u0435\u0442 \u0437\u0430\u043f\u0440\u043e\u0441\u043e\u0432',
        noDeleteError: '\u041e\u0448\u0438\u0431\u043a\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f',

        welcome: '\u041e\u0447\u0435\u0440\u0435\u0434\u044c \u043e\u043d\u043b\u0430\u0439\u043d.',
    },
    en: {
        back: '\u2190 Back',
        backHome: '\u2190 Home',
        savedQueues: 'Your queues',
        deletedQueues: 'Deleted queues',
        organizer: 'Organizer',
        participant: 'Participant',
        createQueue: 'Create queue',
        createQueueDesc: 'Configure and share a link',
        joinQueue: 'Join queue',
        joinQueueDesc: 'Enter a 4-digit code',
        enter: 'Enter',
        feature1Title: 'Fast',
        feature1Desc: 'Queue in 10 seconds',
        feature2Title: 'Simple',
        feature2Desc: 'No registration',
        feature3Title: 'Convenient',
        feature3Desc: 'QR code or 4-digit code',
        or: 'or',

        createTitle: 'Create queue',
        nameLabel: 'Name *',
        namePlaceholder: 'Exam, check-in...',
        descLabel: 'Description',
        descPlaceholder: 'Optional',
        maxPeople: 'Max people',
        perSlot: 'People per slot',
        perSlotHint: 'How many at one time',
        allowDelay: 'Allow "running late"',
        allowSwap: 'Allow slot/seat swap',
        useTimeSlots: 'With time slots',
        slotsConfig: 'Slots',
        startTime: 'Start time',
        slotDuration: 'Slot duration (min)',
        participantInfo: 'Info for participants',
        infoPlaceholder: 'Room 301, bring passport...',
        windowLabel: 'Late window (min)',
        latePolicy: 'Late arrivals',
        toEnd: 'Move to end',
        discard: 'Remove',
        create: 'Create',

        joinTitle: 'Inline \u2014 Join',
        alreadyJoined: 'Already in queue',
        continue: 'Continue',
        loginOther: 'Login as another',
        yourName: 'Your name *',
        namePlaceholder2: 'How should we address you?',
        joinBtn: 'Join queue',
        max: 'Max:',
        swapEnabled: 'Swap on',
        delayEnabled: 'Late ok',

        queueCode: 'Queue code',
        clickToCopy: 'click to copy',
        copied: 'Copied',
        copyError: 'Error',
        copy: 'Copy',
        saved: 'Saved',

        pause: 'Pause',
        resume: 'Resume',
        reopen: 'Reopen',
        close: 'Close',
        callNext: 'Call next',
        exportXlsx: 'Export XLSX',
        deleteQueue: 'Delete queue',
        settings: 'Settings',
        save: 'Save',
        slots: 'Slots',
        inQueue: 'in queue',
        you: 'you',
        allParticipants: 'All participants',
        noSlotParticipants: 'No participants in this slot',
        served: 'Served / Skipped',
        emptyQueue: 'Queue is empty',
        called: 'Called',
        delayed: 'Running late',
        servedStatus: 'Served',
        skipped: 'Skipped',
        servedTitle: 'Serve',
        skipTitle: 'Skip',
        undoTitle: 'Undo',
        undo: 'Undo',
        selected: 'selected',
        move: 'Move',
        deselect: 'Deselect',
        loading: 'Loading...',

        swapRequests: 'Swap requests',
        swapHint: 'Use slot/position swap only for valid reasons. Frequent requests cause inconvenience.',
        swapSlot: 'Swap slot',
        swapPosition: 'Position in slot',
        selectSwapUser: 'Select participant to swap slots',
        selectPosUser: 'Select participant to swap positions',
        sendRequest: 'Send request',
        noParticipants: 'No available participants',
        noSlotParticipants2: 'No participants in slot',
        swapDone: 'Swap completed!',

        positionLabel: 'Your position',
        positionInSlot: 'Position in slot:',
        yourSlot: 'Your slot',
        itsYourTurn: 'It\'s your turn!',
        youCalled: 'Called',
        youServed: 'You\'ve been served',
        statusWaiting: 'Waiting',
        delayedBtn: 'Running late',
        leaveQueue: 'Leave queue',
        schedule: 'Schedule',
        emptyList: 'No one yet',
        inSlot: 'in slot',

        incomingSwap: 'Swap request',
        accept: 'Accept',
        reject: 'Reject',
        cancel: 'Cancel',
        yourRequest: 'Your request:',
        confirmLeave: 'Leave queue? You will be removed from the list.',
        confirmClose: 'Close queue?',
        confirmDelete: 'Delete queue forever? This cannot be undone.',
        undoHint: 'Person served',
        undoSkip: 'Person skipped',
        slotFull: 'Slot is full',
        notFound: 'Queue not found',
        error: 'Error',
        newParticipant: 'New participant:',
        personDelayed: ' is running late',
        newSwapRequest: 'New swap request',
        noRequests: 'No requests',
        noDeleteError: 'Delete error',

        welcome: 'Online queue.',
    }
};

function t(key) {
    const lang = localStorage.getItem(LANG_KEY) || 'ru';
    return (I18N[lang] && I18N[lang][key]) || (I18N.ru[key]) || key;
}

function getLang() {
    return localStorage.getItem(LANG_KEY) || 'ru';
}

function setLang(lang) {
    localStorage.setItem(LANG_KEY, lang);
    location.reload();
}

function translatePage() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const val = t(key);
        if (el.tagName === 'INPUT' && el.type !== 'submit') {
            if (el.placeholder !== undefined) el.placeholder = val;
        } else {
            el.textContent = val;
        }
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        el.placeholder = t(el.getAttribute('data-i18n-placeholder'));
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        el.title = t(el.getAttribute('data-i18n-title'));
    });
}

function langToggleHTML() {
    const cur = getLang();
    const other = cur === 'ru' ? 'EN' : 'RU';
    const otherLang = cur === 'ru' ? 'en' : 'ru';
    return '<button class="lang-toggle" onclick="setLang(\'' + otherLang + '\')">' + other + '</button>';
}
