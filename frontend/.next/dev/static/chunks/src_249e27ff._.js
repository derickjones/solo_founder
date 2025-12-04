(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/src/components/Sidebar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Sidebar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronDownIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDownIcon$3e$__ = __turbopack_context__.i("[project]/node_modules/@heroicons/react/24/outline/esm/ChevronDownIcon.js [app-client] (ecmascript) <export default as ChevronDownIcon>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronUpIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronUpIcon$3e$__ = __turbopack_context__.i("[project]/node_modules/@heroicons/react/24/outline/esm/ChevronUpIcon.js [app-client] (ecmascript) <export default as ChevronUpIcon>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$XMarkIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__XMarkIcon$3e$__ = __turbopack_context__.i("[project]/node_modules/@heroicons/react/24/outline/esm/XMarkIcon.js [app-client] (ecmascript) <export default as XMarkIcon>");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
function Sidebar({ selectedSources, setSelectedSources, sourceCount, setSourceCount, isOpen, setIsOpen }) {
    _s();
    const [generalConferenceOpen, setGeneralConferenceOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false); // Collapsed by default
    const [standardWorksOpen, setStandardWorksOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false); // Collapsed by default
    const handleSourceToggle = (source)=>{
        if (selectedSources.includes(source)) {
            setSelectedSources(selectedSources.filter((s)=>s !== source));
        } else {
            setSelectedSources([
                ...selectedSources,
                source
            ]);
        }
    };
    const getConferenceSources = ()=>[
            'general-conference',
            'gc-year-2025',
            'gc-year-2024',
            'gc-year-2023',
            'gc-year-2022',
            'gc-year-2021',
            'gc-year-2020',
            'gc-year-2019',
            'gc-year-2018',
            'gc-year-2017',
            'gc-year-2016',
            'gc-year-2015',
            'gc-speaker-russell-m-nelson',
            'gc-speaker-dallin-h-oaks',
            'gc-speaker-henry-b-eyring',
            'gc-speaker-jeffrey-r-holland',
            'gc-speaker-dieter-f-uchtdorf',
            'gc-speaker-david-a-bednar',
            'gc-speaker-quentin-l-cook',
            'gc-speaker-d-todd-christofferson',
            'gc-speaker-neil-l-andersen',
            'gc-speaker-ronald-a-rasband',
            'gc-speaker-gary-e-stevenson',
            'gc-speaker-dale-g-renlund'
        ];
    const isAllConferenceSelected = ()=>{
        const conferenceSources = getConferenceSources();
        const selectedConferenceSources = selectedSources.filter((source)=>conferenceSources.includes(source));
        return selectedConferenceSources.length >= conferenceSources.length * 0.8;
    };
    const handleToggleAllConference = ()=>{
        const conferenceSources = getConferenceSources();
        if (isAllConferenceSelected()) {
            // Deselect all conference sources
            setSelectedSources(selectedSources.filter((source)=>!conferenceSources.includes(source)));
        } else {
            // Select all conference sources
            const otherSources = selectedSources.filter((source)=>!conferenceSources.includes(source));
            setSelectedSources([
                ...otherSources,
                ...conferenceSources
            ]);
        }
    };
    const getScriptureSources = ()=>[
            'book-of-mormon',
            'doctrine-and-covenants',
            'pearl-of-great-price',
            'old-testament',
            'new-testament'
        ];
    const isAllScripturesSelected = ()=>{
        const scriptureSources = getScriptureSources();
        const selectedScriptureSources = selectedSources.filter((source)=>scriptureSources.includes(source));
        return selectedScriptureSources.length >= scriptureSources.length * 0.8;
    };
    const isOnlyConferenceSelected = ()=>{
        const conferenceSources = getConferenceSources();
        const scriptureSources = getScriptureSources();
        const allSources = [
            ...conferenceSources,
            ...scriptureSources
        ];
        // Check if only conference sources are selected
        const selectedConferenceSources = selectedSources.filter((source)=>conferenceSources.includes(source));
        const selectedScriptureSources = selectedSources.filter((source)=>scriptureSources.includes(source));
        return selectedConferenceSources.length > 0 && selectedScriptureSources.length === 0;
    };
    const isOnlyScripturesSelected = ()=>{
        const conferenceSources = getConferenceSources();
        const scriptureSources = getScriptureSources();
        // Check if only scripture sources are selected
        const selectedConferenceSources = selectedSources.filter((source)=>conferenceSources.includes(source));
        const selectedScriptureSources = selectedSources.filter((source)=>scriptureSources.includes(source));
        return selectedScriptureSources.length > 0 && selectedConferenceSources.length === 0;
    };
    const handleToggleAllScriptures = ()=>{
        const scriptureSources = getScriptureSources();
        if (isAllScripturesSelected()) {
            // Deselect all scripture sources
            setSelectedSources(selectedSources.filter((source)=>!scriptureSources.includes(source)));
        } else {
            // Select all scripture sources
            const otherSources = selectedSources.filter((source)=>!scriptureSources.includes(source));
            setSelectedSources([
                ...otherSources,
                ...scriptureSources
            ]);
        }
    };
    const handleSelectGeneralConference = ()=>{
        const conferenceSources = getConferenceSources();
        setSelectedSources(conferenceSources);
    };
    const handleSelectStandardWorks = ()=>{
        const scriptureSources = getScriptureSources();
        setSelectedSources(scriptureSources);
    };
    const handleSelectBoth = ()=>{
        const conferenceSources = getConferenceSources();
        const scriptureSources = getScriptureSources();
        setSelectedSources([
            ...conferenceSources,
            ...scriptureSources
        ]);
    };
    const handleToggleSelectAll = ()=>{
        const allSources = [
            // General Conference
            'general-conference',
            // By Year
            'gc-year-2025',
            'gc-year-2024',
            'gc-year-2023',
            'gc-year-2022',
            'gc-year-2021',
            'gc-year-2020',
            'gc-year-2019',
            'gc-year-2018',
            'gc-year-2017',
            'gc-year-2016',
            'gc-year-2015',
            // By Speaker
            'gc-speaker-russell-m-nelson',
            'gc-speaker-dallin-h-oaks',
            'gc-speaker-henry-b-eyring',
            'gc-speaker-jeffrey-r-holland',
            'gc-speaker-dieter-f-uchtdorf',
            'gc-speaker-david-a-bednar',
            'gc-speaker-quentin-l-cook',
            'gc-speaker-d-todd-christofferson',
            'gc-speaker-neil-l-andersen',
            'gc-speaker-ronald-a-rasband',
            'gc-speaker-gary-e-stevenson',
            'gc-speaker-dale-g-renlund',
            // Standard Works
            'book-of-mormon',
            'doctrine-and-covenants',
            'pearl-of-great-price',
            'old-testament',
            'new-testament'
        ];
        // If most sources are selected, deselect all. Otherwise, select all.
        if (selectedSources.length >= allSources.length * 0.8) {
            setSelectedSources([]);
        } else {
            setSelectedSources(allSources);
        }
    };
    const isAllSelected = ()=>{
        const allSources = [
            'general-conference',
            'gc-year-2025',
            'gc-year-2024',
            'gc-year-2023',
            'gc-year-2022',
            'gc-year-2021',
            'gc-year-2020',
            'gc-year-2019',
            'gc-year-2018',
            'gc-year-2017',
            'gc-year-2016',
            'gc-year-2015',
            'gc-speaker-russell-m-nelson',
            'gc-speaker-dallin-h-oaks',
            'gc-speaker-henry-b-eyring',
            'gc-speaker-jeffrey-r-holland',
            'gc-speaker-dieter-f-uchtdorf',
            'gc-speaker-david-a-bednar',
            'gc-speaker-quentin-l-cook',
            'gc-speaker-d-todd-christofferson',
            'gc-speaker-neil-l-andersen',
            'gc-speaker-ronald-a-rasband',
            'gc-speaker-gary-e-stevenson',
            'gc-speaker-dale-g-renlund',
            'book-of-mormon',
            'doctrine-and-covenants',
            'pearl-of-great-price',
            'old-testament',
            'new-testament'
        ];
        return selectedSources.length >= allSources.length * 0.8;
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: `
      w-72 lg:w-80 bg-neutral-800 border-r border-neutral-700 flex flex-col
      fixed lg:relative top-0 left-0 h-full z-30 transition-transform duration-300 ease-in-out
      ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
    `,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-6 border-b border-neutral-700",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex items-center justify-between",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center space-x-3",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "w-8 h-8 rounded-lg overflow-hidden border border-neutral-600",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                                        src: "/christ.jpeg",
                                        alt: "Gospel Study Logo",
                                        className: "w-full h-full object-cover"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 174,
                                        columnNumber: 15
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/src/components/Sidebar.tsx",
                                    lineNumber: 173,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                    className: "text-xl font-semibold text-white",
                                    children: "Gospel Study"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/Sidebar.tsx",
                                    lineNumber: 180,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/Sidebar.tsx",
                            lineNumber: 172,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: ()=>setIsOpen(false),
                            className: "lg:hidden text-neutral-400 hover:text-white p-1",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$XMarkIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__XMarkIcon$3e$__["XMarkIcon"], {
                                className: "w-6 h-6"
                            }, void 0, false, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 187,
                                columnNumber: 13
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/src/components/Sidebar.tsx",
                            lineNumber: 183,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/Sidebar.tsx",
                    lineNumber: 171,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/Sidebar.tsx",
                lineNumber: 170,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-4 lg:p-6 space-y-4 overflow-y-auto flex-1",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-3",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-center justify-between",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                    className: "text-sm text-neutral-400",
                                    children: "Sources to search:"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/Sidebar.tsx",
                                    lineNumber: 196,
                                    columnNumber: 13
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 195,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex flex-wrap gap-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleToggleSelectAll,
                                        className: `text-xs px-3 py-1 rounded transition-colors ${isAllSelected() ? 'bg-blue-600 text-white' : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'}`,
                                        children: "Select All"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 201,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleSelectGeneralConference,
                                        className: `text-xs px-3 py-1 rounded transition-colors ${isOnlyConferenceSelected() ? 'bg-blue-600 text-white' : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'}`,
                                        children: "General Conference"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 211,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleSelectStandardWorks,
                                        className: `text-xs px-3 py-1 rounded transition-colors ${isOnlyScripturesSelected() ? 'bg-blue-600 text-white' : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'}`,
                                        children: "Scriptures"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 221,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 200,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "text-2xl font-bold text-white",
                                children: sourceCount
                            }, void 0, false, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 233,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "relative",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                        type: "range",
                                        min: "1",
                                        max: "20",
                                        value: sourceCount,
                                        onChange: (e)=>setSourceCount(parseInt(e.target.value)),
                                        className: "w-full h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer slider",
                                        style: {
                                            background: `linear-gradient(to right, #525252 0%, #525252 ${(sourceCount - 1) * 5.26}%, #374151 ${(sourceCount - 1) * 5.26}%, #374151 100%)`
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 237,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex justify-between text-xs text-neutral-500 mt-1",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: "1"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 249,
                                                columnNumber: 15
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: "20"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 250,
                                                columnNumber: 15
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 248,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 236,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/Sidebar.tsx",
                        lineNumber: 194,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "text-sm text-neutral-400 mt-4",
                        children: "Select your sources"
                    }, void 0, false, {
                        fileName: "[project]/src/components/Sidebar.tsx",
                        lineNumber: 255,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>setGeneralConferenceOpen(!generalConferenceOpen),
                                className: "w-full flex items-center justify-between p-3 bg-neutral-700 rounded-lg hover:bg-neutral-600 transition-colors",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex items-center space-x-3",
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            className: "text-white text-sm",
                                            children: "General Conference"
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/Sidebar.tsx",
                                            lineNumber: 266,
                                            columnNumber: 15
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 265,
                                        columnNumber: 13
                                    }, this),
                                    generalConferenceOpen ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronUpIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronUpIcon$3e$__["ChevronUpIcon"], {
                                        className: "w-4 h-4 text-neutral-400"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 269,
                                        columnNumber: 15
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronDownIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDownIcon$3e$__["ChevronDownIcon"], {
                                        className: "w-4 h-4 text-neutral-400"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 271,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 261,
                                columnNumber: 11
                            }, this),
                            generalConferenceOpen && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "ml-6 space-y-3",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                        className: "flex items-center space-x-2 text-sm text-neutral-300",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                type: "checkbox",
                                                checked: selectedSources.includes('general-conference'),
                                                onChange: ()=>handleSourceToggle('general-conference'),
                                                className: "rounded"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 279,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: "All Sessions (2015-2025)"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 285,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 278,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "space-y-1",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "text-xs text-neutral-400 font-medium",
                                                children: "By Year:"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 290,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "grid grid-cols-2 gap-1",
                                                children: [
                                                    2025,
                                                    2024,
                                                    2023,
                                                    2022,
                                                    2021,
                                                    2020,
                                                    2019,
                                                    2018,
                                                    2017,
                                                    2016,
                                                    2015
                                                ].map((year)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                        className: "flex items-center space-x-1 text-xs text-neutral-300",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                type: "checkbox",
                                                                checked: selectedSources.includes(`gc-year-${year}`),
                                                                onChange: ()=>handleSourceToggle(`gc-year-${year}`),
                                                                className: "rounded text-xs"
                                                            }, void 0, false, {
                                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                                lineNumber: 294,
                                                                columnNumber: 23
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                children: year
                                                            }, void 0, false, {
                                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                                lineNumber: 300,
                                                                columnNumber: 23
                                                            }, this)
                                                        ]
                                                    }, year, true, {
                                                        fileName: "[project]/src/components/Sidebar.tsx",
                                                        lineNumber: 293,
                                                        columnNumber: 21
                                                    }, this))
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 291,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 289,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "space-y-1",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "text-xs text-neutral-400 font-medium",
                                                children: "By Speaker:"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 308,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "space-y-1",
                                                children: [
                                                    'Russell M. Nelson',
                                                    'Dallin H. Oaks',
                                                    'Henry B. Eyring',
                                                    'Jeffrey R. Holland',
                                                    'Dieter F. Uchtdorf',
                                                    'David A. Bednar',
                                                    'Quentin L. Cook',
                                                    'D. Todd Christofferson',
                                                    'Neil L. Andersen',
                                                    'Ronald A. Rasband',
                                                    'Gary E. Stevenson',
                                                    'Dale G. Renlund'
                                                ].map((speaker)=>{
                                                    const speakerKey = `gc-speaker-${speaker.toLowerCase().replace(/\s+/g, '-').replace('.', '')}`;
                                                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                        className: "flex items-center space-x-1 text-xs text-neutral-300",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                                type: "checkbox",
                                                                checked: selectedSources.includes(speakerKey),
                                                                onChange: ()=>handleSourceToggle(speakerKey),
                                                                className: "rounded text-xs"
                                                            }, void 0, false, {
                                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                                lineNumber: 327,
                                                                columnNumber: 25
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                children: speaker
                                                            }, void 0, false, {
                                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                                lineNumber: 333,
                                                                columnNumber: 25
                                                            }, this)
                                                        ]
                                                    }, speaker, true, {
                                                        fileName: "[project]/src/components/Sidebar.tsx",
                                                        lineNumber: 326,
                                                        columnNumber: 23
                                                    }, this);
                                                })
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 309,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 307,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 276,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/Sidebar.tsx",
                        lineNumber: 260,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "space-y-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>setStandardWorksOpen(!standardWorksOpen),
                                className: "w-full flex items-center justify-between p-3 bg-neutral-700 rounded-lg hover:bg-neutral-600 transition-colors",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex items-center space-x-3",
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            className: "text-white text-sm",
                                            children: "Standard Works"
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/Sidebar.tsx",
                                            lineNumber: 350,
                                            columnNumber: 15
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 349,
                                        columnNumber: 13
                                    }, this),
                                    standardWorksOpen ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronUpIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronUpIcon$3e$__["ChevronUpIcon"], {
                                        className: "w-4 h-4 text-neutral-400"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 353,
                                        columnNumber: 15
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronDownIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDownIcon$3e$__["ChevronDownIcon"], {
                                        className: "w-4 h-4 text-neutral-400"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 355,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 345,
                                columnNumber: 11
                            }, this),
                            standardWorksOpen && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "ml-6 space-y-2",
                                children: [
                                    'Book of Mormon',
                                    'Doctrine & Covenants',
                                    'Pearl of Great Price',
                                    'Old Testament',
                                    'New Testament'
                                ].map((work)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                        className: "flex items-center space-x-2 text-sm text-neutral-300",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                type: "checkbox",
                                                checked: selectedSources.includes(work.toLowerCase().replace(/\s+/g, '-').replace('&', 'and')),
                                                onChange: ()=>handleSourceToggle(work.toLowerCase().replace(/\s+/g, '-').replace('&', 'and')),
                                                className: "rounded"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 369,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                children: work
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/Sidebar.tsx",
                                                lineNumber: 375,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, work, true, {
                                        fileName: "[project]/src/components/Sidebar.tsx",
                                        lineNumber: 368,
                                        columnNumber: 17
                                    }, this))
                            }, void 0, false, {
                                fileName: "[project]/src/components/Sidebar.tsx",
                                lineNumber: 360,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/Sidebar.tsx",
                        lineNumber: 344,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Sidebar.tsx",
                lineNumber: 193,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Sidebar.tsx",
        lineNumber: 164,
        columnNumber: 5
    }, this);
}
_s(Sidebar, "PvFVl+76OQ8WBnLZoTIojk65aec=");
_c = Sidebar;
var _c;
__turbopack_context__.k.register(_c, "Sidebar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/services/api.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "askQuestionStream",
    ()=>askQuestionStream,
    "getAvailableSources",
    ()=>getAvailableSources,
    "getHealth",
    ()=>getHealth,
    "searchScriptures",
    ()=>searchScriptures
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
const API_BASE_URL = ("TURBOPACK compile-time value", "https://gospel-guide-api-273320302933.us-central1.run.app") || 'https://gospel-guide-api-273320302933.us-central1.run.app';
// Map frontend modes to API modes
const MODE_MAPPING = {
    'AI Q&A': 'default',
    'Scripture Study': 'default',
    'General Conference': 'general-conference-only',
    'Book of Mormon': 'book-of-mormon-only',
    'Come Follow Me': 'come-follow-me',
    'Youth Mode': 'youth',
    'Scholar Mode': 'scholar'
};
// Map selected sources to API source filters
const getSourceFilter = (selectedSources)=>{
    // If no sources selected, return undefined (search all)
    if (selectedSources.length === 0) {
        return undefined;
    }
    // If all sources are selected (common case), don't filter
    const allSources = [
        'general-conference',
        'gc-year-2025',
        'gc-year-2024',
        'gc-year-2023',
        'gc-year-2022',
        'gc-year-2021',
        'gc-year-2020',
        'gc-year-2019',
        'gc-year-2018',
        'gc-year-2017',
        'gc-year-2016',
        'gc-year-2015',
        'gc-speaker-russell-m-nelson',
        'gc-speaker-dallin-h-oaks',
        'gc-speaker-henry-b-eyring',
        'gc-speaker-jeffrey-r-holland',
        'gc-speaker-dieter-f-uchtdorf',
        'gc-speaker-david-a-bednar',
        'gc-speaker-quentin-l-cook',
        'gc-speaker-d-todd-christofferson',
        'gc-speaker-neil-l-andersen',
        'gc-speaker-ronald-a-rasband',
        'gc-speaker-gary-e-stevenson',
        'gc-speaker-dale-g-renlund',
        'book-of-mormon',
        'doctrine-and-covenants',
        'pearl-of-great-price',
        'old-testament',
        'new-testament'
    ];
    if (selectedSources.length === allSources.length) {
        return undefined; // Search all sources
    }
    // For now, build a single filter from the most specific selection
    // Priority: specific year/speaker filters > general conference > scripture works
    // Check for specific General Conference filters first
    const yearFilters = selectedSources.filter((s)=>s.startsWith('gc-year-'));
    if (yearFilters.length === 1) {
        const year = parseInt(yearFilters[0].replace('gc-year-', ''));
        return {
            source_type: 'conference',
            year
        };
    }
    const speakerFilters = selectedSources.filter((s)=>s.startsWith('gc-speaker-'));
    if (speakerFilters.length === 1) {
        const speakerKey = speakerFilters[0].replace('gc-speaker-', '');
        const speakerName = speakerKey.replace(/-/g, ' ').replace(/\b\w/g, (l)=>l.toUpperCase()); // Convert to Title Case
        return {
            source_type: 'conference',
            speaker: speakerName
        };
    }
    // Check for general conference
    if (selectedSources.includes('general-conference')) {
        return {
            source_type: 'conference'
        };
    }
    // Check for specific scripture works
    const scriptureMap = {
        'book-of-mormon': 'Book of Mormon',
        'doctrine-and-covenants': 'Doctrine and Covenants',
        'pearl-of-great-price': 'Pearl of Great Price',
        'old-testament': 'Old Testament',
        'new-testament': 'New Testament'
    };
    const scriptureWorks = selectedSources.filter((s)=>scriptureMap[s]);
    if (scriptureWorks.length === 1) {
        return {
            source_type: 'scripture',
            standard_work: scriptureMap[scriptureWorks[0]]
        };
    }
    // If multiple scripture works selected, filter by scripture type only
    if (scriptureWorks.length > 1) {
        return {
            source_type: 'scripture'
        };
    }
    // Default: no filter (search all)
    return undefined;
};
const searchScriptures = async (request)=>{
    const apiMode = MODE_MAPPING[request.mode || 'AI Q&A'] || 'default';
    const sourceFilter = request.selectedSources ? getSourceFilter(request.selectedSources) : undefined;
    const body = {
        query: request.query,
        mode: apiMode,
        top_k: request.max_results || 5,
        ...sourceFilter && {
            source_filter: sourceFilter
        }
    };
    const response = await fetch(`${API_BASE_URL}/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Search failed: ${response.statusText} - ${errorText}`);
    }
    const data = await response.json();
    // Transform the API response to match our expected format
    return {
        query: data.query,
        results: data.results.map((result)=>({
                content: result.content,
                source: result.metadata?.standard_work || 'Unknown',
                book: result.metadata?.book || result.metadata?.title,
                chapter: result.metadata?.chapter,
                verse: result.metadata?.verse,
                score: result.score,
                citation: result.metadata?.citation,
                url: result.metadata?.url,
                speaker: result.metadata?.speaker,
                year: result.metadata?.year,
                session: result.metadata?.session,
                title: result.metadata?.title,
                paragraph: result.metadata?.paragraph,
                rank: result.rank
            })),
        total_found: data.total_found,
        search_time: data.search_time_ms / 1000,
        mode: data.mode
    };
};
const askQuestionStream = async (request, onChunk)=>{
    const apiMode = MODE_MAPPING[request.mode || 'AI Q&A'] || 'default';
    const sourceFilter = request.selectedSources ? getSourceFilter(request.selectedSources) : undefined;
    const body = {
        query: request.query,
        mode: apiMode,
        top_k: request.max_results || 10,
        ...sourceFilter && {
            source_filter: sourceFilter
        }
    };
    console.log('Streaming request body:', body);
    const response = await fetch(`${API_BASE_URL}/ask/stream`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    console.log('Streaming response status:', response.status, response.statusText);
    if (!response.ok) {
        throw new Error(`Streaming request failed: ${response.statusText}`);
    }
    if (!response.body) {
        throw new Error('Response body is null');
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    console.log('Starting to read streaming response...');
    try {
        while(true){
            const { done, value } = await reader.read();
            if (done) {
                console.log('Streaming complete');
                break;
            }
            // Add new chunk to buffer
            buffer += decoder.decode(value, {
                stream: true
            });
            // Split buffer on double newlines (SSE message boundaries)
            const messages = buffer.split('\n\n');
            // Keep the last partial message in buffer
            buffer = messages.pop() || '';
            // Process complete messages
            for (const message of messages){
                const lines = message.split('\n');
                for (const line of lines){
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            console.log('Received chunk:', data.type, data.content ? data.content.slice(0, 50) + '...' : '');
                            // Transform sources to match our expected format
                            if (data.type === 'sources' && data.sources) {
                                data.sources = data.sources.map((source)=>({
                                        content: source.content,
                                        source: source.metadata?.standard_work || 'Unknown',
                                        book: source.metadata?.book || source.metadata?.title,
                                        chapter: source.metadata?.chapter,
                                        verse: source.metadata?.verse,
                                        score: source.score,
                                        citation: source.metadata?.citation,
                                        url: source.metadata?.url,
                                        speaker: source.metadata?.speaker,
                                        year: source.metadata?.year,
                                        session: source.metadata?.session,
                                        title: source.metadata?.title,
                                        paragraph: source.metadata?.paragraph,
                                        rank: source.rank
                                    }));
                            }
                            onChunk(data);
                        } catch (e) {
                            console.error('Failed to parse SSE data:', e, 'Line:', line);
                        }
                    }
                }
            }
        }
    } finally{
        reader.releaseLock();
    }
};
const getAvailableSources = async ()=>{
    const response = await fetch(`${API_BASE_URL}/sources`);
    if (!response.ok) {
        throw new Error(`Failed to fetch sources: ${response.statusText}`);
    }
    return response.json();
};
const getHealth = async ()=>{
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
        throw new Error(`Health check failed: ${response.statusText}`);
    }
    const data = await response.json();
    return {
        status: data.status,
        segments_loaded: data.total_segments
    };
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/components/ChatInterface.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>ChatInterface
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronDownIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDownIcon$3e$__ = __turbopack_context__.i("[project]/node_modules/@heroicons/react/24/outline/esm/ChevronDownIcon.js [app-client] (ecmascript) <export default as ChevronDownIcon>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$PaperAirplaneIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__PaperAirplaneIcon$3e$__ = __turbopack_context__.i("[project]/node_modules/@heroicons/react/24/outline/esm/PaperAirplaneIcon.js [app-client] (ecmascript) <export default as PaperAirplaneIcon>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$Bars3Icon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Bars3Icon$3e$__ = __turbopack_context__.i("[project]/node_modules/@heroicons/react/24/outline/esm/Bars3Icon.js [app-client] (ecmascript) <export default as Bars3Icon>");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$services$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/services/api.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$markdown$2f$lib$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__Markdown__as__default$3e$__ = __turbopack_context__.i("[project]/node_modules/react-markdown/lib/index.js [app-client] (ecmascript) <export Markdown as default>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
;
function ChatInterface({ selectedSources, sourceCount, sidebarOpen, setSidebarOpen }) {
    _s();
    const [query, setQuery] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    const [mode, setMode] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('AI Q&A');
    const [modeDropdownOpen, setModeDropdownOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [messages, setMessages] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    // Format citations from individual metadata fields
    const formatCitation = (result)=>{
        if (result.speaker && result.title) {
            // Conference talk format: Speaker, "Title", Session Year, ¶#
            let citation = `${result.speaker}, "${result.title}"`;
            if (result.session && result.year) {
                citation += `, ${result.session} ${result.year}`;
            }
            if (result.paragraph) {
                citation += `, ¶${result.paragraph}`;
            }
            return citation;
        } else if (result.book && result.chapter) {
            // Scripture format: Standard Work Book Chapter:Verse
            return `${result.source} ${result.book} ${result.chapter}${result.verse ? `:${result.verse}` : ''}`;
        } else if (result.source) {
            // Fallback to source name
            return result.source;
        }
        // Last resort - use cleaned original citation
        return result.citation?.replace(/^\((.+)\)$/, '$1') || 'Unknown Source';
    };
    // Format text for better readability
    const formatText = (text)=>{
        return text// Split on sentence endings followed by capitals (new topics)
        .replace(/(\. )([A-Z][a-z])/g, '$1\n\n$2')// Split on numbered points
        .replace(/(\d+\. )/g, '\n\n$1')// Split on quotes that start new thoughts  
        .replace(/(") ([A-Z])/g, '$1\n\n$2')// Split on scripture citations in parentheses followed by new thoughts
        .replace(/(\([^)]+\)\. )([A-Z])/g, '$1\n\n$2')// Split on long sentences for readability
        .replace(/([.!?]) ([A-Z][^.!?]{50,})/g, '$1\n\n$2')// Clean up extra spaces and normalize
        .replace(/\n{3,}/g, '\n\n').trim();
    };
    const modes = [
        'AI Q&A',
        'Scripture Study',
        'General Conference',
        'Book of Mormon',
        'Come Follow Me',
        'Youth Mode',
        'Scholar Mode'
    ];
    const handleSubmit = async (e)=>{
        e.preventDefault();
        if (!query.trim() || isLoading) return;
        // Add user message
        const userMessage = {
            id: Date.now(),
            type: 'user',
            content: query
        };
        setMessages((prev)=>[
                ...prev,
                userMessage
            ]);
        setIsLoading(true);
        const searchQuery = query;
        setQuery('');
        // Create assistant message that will be updated as we stream
        const assistantMessageId = Date.now() + 1;
        const initialAssistantMessage = {
            id: assistantMessageId,
            type: 'assistant',
            content: '',
            results: [],
            searchTime: 0,
            isStreaming: true
        };
        setMessages((prev)=>[
                ...prev,
                initialAssistantMessage
            ]);
        try {
            let fullAnswer = '';
            let sources = [];
            let searchTime = 0;
            let lastUpdateTime = 0;
            const UPDATE_THROTTLE = 50; // Update UI every 50ms max
            await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$services$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["askQuestionStream"])({
                query: searchQuery,
                mode,
                max_results: sourceCount,
                selectedSources
            }, (chunk)=>{
                console.log('Received chunk in ChatInterface:', chunk.type, chunk.content ? chunk.content.slice(0, 30) + '...' : '');
                switch(chunk.type){
                    case 'search_complete':
                        searchTime = (chunk.search_time_ms || 0) / 1000;
                        setMessages((prev)=>prev.map((msg)=>msg.id === assistantMessageId ? {
                                    ...msg,
                                    content: `✅ Found ${chunk.total_sources || 0} sources. Generating response...`,
                                    searchTime
                                } : msg));
                        break;
                    case 'content':
                        if (chunk.content) {
                            fullAnswer += chunk.content;
                            // Throttle updates for better visual streaming effect
                            const now = Date.now();
                            if (now - lastUpdateTime > UPDATE_THROTTLE) {
                                lastUpdateTime = now;
                                setMessages((prev)=>prev.map((msg)=>msg.id === assistantMessageId ? {
                                            ...msg,
                                            content: fullAnswer
                                        } : msg));
                            }
                        }
                        break;
                    case 'sources':
                        if (chunk.sources) {
                            sources = chunk.sources;
                            setMessages((prev)=>prev.map((msg)=>msg.id === assistantMessageId ? {
                                        ...msg,
                                        results: sources
                                    } : msg));
                        }
                        break;
                    case 'done':
                        // Make sure final content is displayed and mark streaming as complete
                        setMessages((prev)=>prev.map((msg)=>msg.id === assistantMessageId ? {
                                    ...msg,
                                    content: fullAnswer,
                                    isStreaming: false
                                } : msg));
                        setIsLoading(false);
                        break;
                    case 'error':
                        setMessages((prev)=>prev.map((msg)=>msg.id === assistantMessageId ? {
                                    ...msg,
                                    content: `Sorry, I encountered an error: ${chunk.error}`,
                                    isStreaming: false
                                } : msg));
                        setIsLoading(false);
                        break;
                }
            });
        } catch (error) {
            setMessages((prev)=>prev.map((msg)=>msg.id === assistantMessageId ? {
                        ...msg,
                        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}`,
                        isStreaming: false
                    } : msg));
            setIsLoading(false);
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex-1 flex flex-col bg-neutral-900 lg:ml-0",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "lg:hidden flex items-center justify-between p-4 border-b border-neutral-700",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>setSidebarOpen(true),
                        className: "text-neutral-400 hover:text-white p-2",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$Bars3Icon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Bars3Icon$3e$__["Bars3Icon"], {
                            className: "w-6 h-6"
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatInterface.tsx",
                            lineNumber: 200,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/components/ChatInterface.tsx",
                        lineNumber: 196,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                        className: "text-lg font-semibold text-white",
                        children: "Gospel Study"
                    }, void 0, false, {
                        fileName: "[project]/src/components/ChatInterface.tsx",
                        lineNumber: 202,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "w-10"
                    }, void 0, false, {
                        fileName: "[project]/src/components/ChatInterface.tsx",
                        lineNumber: 203,
                        columnNumber: 9
                    }, this),
                    " "
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/ChatInterface.tsx",
                lineNumber: 195,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center justify-center pt-8 lg:pt-16 pb-6 lg:pb-8 px-4",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex flex-col items-center space-y-4 lg:space-y-6",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "w-16 h-16 lg:w-24 lg:h-24 rounded-full overflow-hidden border-2 border-neutral-700",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                                src: "/christ.jpeg",
                                alt: "Gospel Study Assistant Logo",
                                className: "w-full h-full object-cover"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ChatInterface.tsx",
                                lineNumber: 210,
                                columnNumber: 13
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatInterface.tsx",
                            lineNumber: 209,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "text-center",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                    className: "text-2xl lg:text-4xl font-bold text-white mb-2",
                                    children: "Gospel Study Assistant"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 217,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    className: "text-sm lg:text-xl text-neutral-400 px-4",
                                    children: "Gospel study made simple to build faith - for Come Follow Me, lessons, and personal study"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 218,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/ChatInterface.tsx",
                            lineNumber: 216,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ChatInterface.tsx",
                    lineNumber: 208,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/ChatInterface.tsx",
                lineNumber: 207,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "px-4 lg:px-8 pb-4",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "max-w-4xl mx-auto",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                        onSubmit: handleSubmit,
                        className: "relative",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex flex-col sm:flex-row items-stretch sm:items-center bg-neutral-800 border-2 border-neutral-700 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 rounded-2xl p-3 lg:p-4 transition-all duration-200 gap-3 sm:gap-0",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                    type: "text",
                                    value: query,
                                    onChange: (e)=>setQuery(e.target.value),
                                    placeholder: "Ask any gospel question...",
                                    className: "flex-1 bg-transparent text-white placeholder-neutral-400 outline-none text-base lg:text-lg min-w-0"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 228,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "relative sm:mx-4 order-2 sm:order-1",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            type: "button",
                                            onClick: ()=>setModeDropdownOpen(!modeDropdownOpen),
                                            className: "flex items-center justify-center space-x-2 bg-neutral-700 hover:bg-neutral-600 px-3 lg:px-4 py-2 rounded-lg transition-colors w-full sm:w-auto",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "text-white text-xs lg:text-sm",
                                                    children: mode
                                                }, void 0, false, {
                                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                                    lineNumber: 243,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$ChevronDownIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__ChevronDownIcon$3e$__["ChevronDownIcon"], {
                                                    className: "w-4 h-4 text-neutral-400"
                                                }, void 0, false, {
                                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                                    lineNumber: 244,
                                                    columnNumber: 19
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/src/components/ChatInterface.tsx",
                                            lineNumber: 238,
                                            columnNumber: 17
                                        }, this),
                                        modeDropdownOpen && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "absolute top-full right-0 mt-2 bg-neutral-700 rounded-lg shadow-lg border border-neutral-600 py-2 min-w-40",
                                            children: modes.map((modeOption)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                    type: "button",
                                                    onClick: ()=>{
                                                        setMode(modeOption);
                                                        setModeDropdownOpen(false);
                                                    },
                                                    className: "block w-full px-4 py-2 text-left text-white hover:bg-neutral-600 transition-colors text-sm",
                                                    children: modeOption
                                                }, modeOption, false, {
                                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                                    lineNumber: 250,
                                                    columnNumber: 23
                                                }, this))
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ChatInterface.tsx",
                                            lineNumber: 248,
                                            columnNumber: 19
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 237,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    type: "submit",
                                    disabled: !query.trim() || isLoading,
                                    className: "bg-neutral-600 hover:bg-neutral-500 disabled:bg-neutral-700 disabled:cursor-not-allowed p-2 lg:p-3 rounded-full transition-colors order-1 sm:order-2 self-end sm:self-center",
                                    children: isLoading ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "animate-spin rounded-full h-4 w-4 lg:h-5 lg:w-5 border-2 border-white border-t-transparent"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                        lineNumber: 272,
                                        columnNumber: 19
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$heroicons$2f$react$2f$24$2f$outline$2f$esm$2f$PaperAirplaneIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__PaperAirplaneIcon$3e$__["PaperAirplaneIcon"], {
                                        className: "w-4 h-4 lg:w-5 lg:h-5 text-white"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                        lineNumber: 274,
                                        columnNumber: 19
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 266,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/ChatInterface.tsx",
                            lineNumber: 227,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/components/ChatInterface.tsx",
                        lineNumber: 226,
                        columnNumber: 11
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/src/components/ChatInterface.tsx",
                    lineNumber: 225,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/ChatInterface.tsx",
                lineNumber: 224,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex-1 px-4 lg:px-8 pb-4 lg:pb-8 overflow-y-auto",
                children: messages.length > 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "max-w-4xl mx-auto space-y-4 lg:space-y-6",
                    children: [
                        messages.map((message)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "space-y-4",
                                children: [
                                    (message.type === 'user' || message.type === 'assistant' && message.content) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: `p-3 lg:p-4 rounded-lg ${message.type === 'user' ? 'bg-neutral-600 text-white ml-auto max-w-sm lg:max-w-lg' : 'bg-neutral-700 text-white max-w-full'}`,
                                        children: message.type === 'assistant' ? message.content ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "space-y-4 leading-relaxed text-neutral-100 prose prose-invert max-w-none [&>*]:text-neutral-100",
                                            children: message.isStreaming ? // During streaming, use simple text with minimal parsing for better performance
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "text-base leading-7 text-neutral-100 whitespace-pre-wrap",
                                                children: [
                                                    message.content,
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        className: "inline-block w-2 h-4 bg-green-400 animate-pulse ml-1",
                                                        children: "|"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                                        lineNumber: 303,
                                                        columnNumber: 31
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                lineNumber: 301,
                                                columnNumber: 29
                                            }, this) : // After streaming is complete, use full markdown rendering
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$markdown$2f$lib$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__Markdown__as__default$3e$__["default"], {
                                                components: {
                                                    strong: ({ children })=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                            className: "font-bold text-white",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatInterface.tsx",
                                                            lineNumber: 309,
                                                            columnNumber: 59
                                                        }, void 0),
                                                    em: ({ children })=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("em", {
                                                            className: "italic",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatInterface.tsx",
                                                            lineNumber: 310,
                                                            columnNumber: 55
                                                        }, void 0),
                                                    p: ({ children })=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            className: "text-base leading-7 mb-4 text-neutral-100",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatInterface.tsx",
                                                            lineNumber: 311,
                                                            columnNumber: 54
                                                        }, void 0)
                                                },
                                                children: message.content
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                lineNumber: 307,
                                                columnNumber: 29
                                            }, this)
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ChatInterface.tsx",
                                            lineNumber: 298,
                                            columnNumber: 25
                                        }, this) : null : message.content
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                        lineNumber: 289,
                                        columnNumber: 19
                                    }, this),
                                    message.type === 'assistant' && message.results && message.results.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "space-y-3 ml-4",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "text-sm text-neutral-400 font-medium mb-3 border-b border-neutral-700 pb-2",
                                                children: [
                                                    "References (",
                                                    message.results.length,
                                                    ")"
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                lineNumber: 328,
                                                columnNumber: 21
                                            }, this),
                                            message.results.map((result, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    className: "bg-neutral-800 p-4 rounded-lg border border-neutral-600 hover:border-neutral-500 transition-colors",
                                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "flex items-start justify-between gap-4",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                className: "flex-1",
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                        className: "text-sm text-neutral-200 font-medium mb-2",
                                                                        children: formatCitation(result)
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                                                        lineNumber: 336,
                                                                        columnNumber: 29
                                                                    }, this),
                                                                    result.url && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                                                                        href: result.url,
                                                                        target: "_blank",
                                                                        rel: "noopener noreferrer",
                                                                        className: "inline-flex items-center text-xs text-blue-400 hover:text-blue-300 transition-colors",
                                                                        children: [
                                                                            "🔗 Read Full Text",
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                                                                className: "w-3 h-3 ml-1",
                                                                                fill: "none",
                                                                                stroke: "currentColor",
                                                                                viewBox: "0 0 24 24",
                                                                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                                                                    strokeLinecap: "round",
                                                                                    strokeLinejoin: "round",
                                                                                    strokeWidth: 2,
                                                                                    d: "M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                                                                    lineNumber: 350,
                                                                                    columnNumber: 35
                                                                                }, this)
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                                                lineNumber: 349,
                                                                                columnNumber: 33
                                                                            }, this)
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                                                        lineNumber: 342,
                                                                        columnNumber: 31
                                                                    }, this)
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                                lineNumber: 334,
                                                                columnNumber: 27
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                className: "flex flex-col items-end",
                                                                children: [
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                        className: "text-xs text-neutral-400 mb-1",
                                                                        children: "Relevance"
                                                                    }, void 0, false, {
                                                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                                                        lineNumber: 358,
                                                                        columnNumber: 29
                                                                    }, this),
                                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                        className: "flex items-center gap-2",
                                                                        children: [
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                                className: "w-16 h-2 bg-neutral-700 rounded-full overflow-hidden",
                                                                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                                                    className: `h-full rounded-full transition-all ${result.score >= 0.8 ? 'bg-green-500' : result.score >= 0.6 ? 'bg-yellow-500' : 'bg-red-500'}`,
                                                                                    style: {
                                                                                        width: `${Math.max(result.score * 100, 5)}%`
                                                                                    }
                                                                                }, void 0, false, {
                                                                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                                                                    lineNumber: 361,
                                                                                    columnNumber: 33
                                                                                }, this)
                                                                            }, void 0, false, {
                                                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                                                lineNumber: 360,
                                                                                columnNumber: 31
                                                                            }, this),
                                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                                                className: "text-xs text-neutral-400 font-mono",
                                                                                children: [
                                                                                    (result.score * 100).toFixed(0),
                                                                                    "%"
                                                                                ]
                                                                            }, void 0, true, {
                                                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                                                lineNumber: 369,
                                                                                columnNumber: 31
                                                                            }, this)
                                                                        ]
                                                                    }, void 0, true, {
                                                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                                                        lineNumber: 359,
                                                                        columnNumber: 29
                                                                    }, this)
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/src/components/ChatInterface.tsx",
                                                                lineNumber: 357,
                                                                columnNumber: 27
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                                        lineNumber: 333,
                                                        columnNumber: 25
                                                    }, this)
                                                }, index, false, {
                                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                                    lineNumber: 332,
                                                    columnNumber: 23
                                                }, this))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/ChatInterface.tsx",
                                        lineNumber: 327,
                                        columnNumber: 19
                                    }, this)
                                ]
                            }, message.id, true, {
                                fileName: "[project]/src/components/ChatInterface.tsx",
                                lineNumber: 287,
                                columnNumber: 15
                            }, this)),
                        isLoading && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex items-center justify-center p-4",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "animate-spin rounded-full h-8 w-8 border-b-2 border-neutral-500"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 385,
                                    columnNumber: 17
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "ml-3 text-neutral-400",
                                    children: "Searching scriptures..."
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 386,
                                    columnNumber: 17
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/ChatInterface.tsx",
                            lineNumber: 384,
                            columnNumber: 15
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ChatInterface.tsx",
                    lineNumber: 285,
                    columnNumber: 11
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex-1"
                }, void 0, false, {
                    fileName: "[project]/src/components/ChatInterface.tsx",
                    lineNumber: 391,
                    columnNumber: 11
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/ChatInterface.tsx",
                lineNumber: 283,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "px-8 py-4 border-t border-neutral-700",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "max-w-4xl mx-auto flex items-center justify-between text-sm text-neutral-400",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            children: "© 2025 Gospel Study Assistant • AI-powered gospel study"
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatInterface.tsx",
                            lineNumber: 398,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex space-x-6",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                    href: "/terms",
                                    className: "hover:text-white transition-colors",
                                    children: "Terms of Use"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 400,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                    href: "/about",
                                    className: "hover:text-white transition-colors",
                                    children: "About"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ChatInterface.tsx",
                                    lineNumber: 403,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/ChatInterface.tsx",
                            lineNumber: 399,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ChatInterface.tsx",
                    lineNumber: 397,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/ChatInterface.tsx",
                lineNumber: 396,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/ChatInterface.tsx",
        lineNumber: 193,
        columnNumber: 5
    }, this);
}
_s(ChatInterface, "17h9zyEMnHx5oeHlI6lMR+rvuEA=");
_c = ChatInterface;
var _c;
__turbopack_context__.k.register(_c, "ChatInterface");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/app/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Home
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Sidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/Sidebar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ChatInterface$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/ChatInterface.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
function Home() {
    _s();
    // Pre-select all available sources
    const allSources = [
        // General Conference
        'general-conference',
        // By Year
        'gc-year-2025',
        'gc-year-2024',
        'gc-year-2023',
        'gc-year-2022',
        'gc-year-2021',
        'gc-year-2020',
        'gc-year-2019',
        'gc-year-2018',
        'gc-year-2017',
        'gc-year-2016',
        'gc-year-2015',
        // By Speaker
        'gc-speaker-russell-m-nelson',
        'gc-speaker-dallin-h-oaks',
        'gc-speaker-henry-b-eyring',
        'gc-speaker-jeffrey-r-holland',
        'gc-speaker-dieter-f-uchtdorf',
        'gc-speaker-david-a-bednar',
        'gc-speaker-quentin-l-cook',
        'gc-speaker-d-todd-christofferson',
        'gc-speaker-neil-l-andersen',
        'gc-speaker-ronald-a-rasband',
        'gc-speaker-gary-e-stevenson',
        'gc-speaker-dale-g-renlund',
        // Standard Works
        'book-of-mormon',
        'doctrine-and-covenants',
        'pearl-of-great-price',
        'old-testament',
        'new-testament'
    ];
    const [selectedSources, setSelectedSources] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(allSources);
    const [sourceCount, setSourceCount] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(10);
    const [sidebarOpen, setSidebarOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex h-screen bg-gray-900 text-white relative",
        children: [
            sidebarOpen && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden",
                onClick: ()=>setSidebarOpen(false)
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 32,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Sidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                selectedSources: selectedSources,
                setSelectedSources: setSelectedSources,
                sourceCount: sourceCount,
                setSourceCount: setSourceCount,
                isOpen: sidebarOpen,
                setIsOpen: setSidebarOpen
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 38,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ChatInterface$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                selectedSources: selectedSources,
                sourceCount: sourceCount,
                sidebarOpen: sidebarOpen,
                setSidebarOpen: setSidebarOpen
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 46,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/app/page.tsx",
        lineNumber: 29,
        columnNumber: 5
    }, this);
}
_s(Home, "dl4/7l0CquYmbZkNEGtUSQ4HyZ4=");
_c = Home;
var _c;
__turbopack_context__.k.register(_c, "Home");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=src_249e27ff._.js.map