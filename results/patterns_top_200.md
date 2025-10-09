# JavaScript/TypeScript Code Patterns - Top 200

*Generated: 2025-10-09 23:28:10*

---

## 📊 Summary

- **Total Patterns**: 200
- **Total Occurrences**: 3,004,949
- **Repositories Analyzed**: 150

---

## 📑 Table of Contents

- [ARRAY_OPERATIONS](#array-operations) (6 patterns)
- [ASYNC_OPERATIONS](#async-operations) (3 patterns)
- [CONTROL_FLOW](#control-flow) (146 patterns)
- [DATA_FETCHING](#data-fetching) (9 patterns)
- [ERROR_HANDLING](#error-handling) (2 patterns)
- [EXPRESSIONS](#expressions) (12 patterns)
- [FUNCTION_CALLS](#function-calls) (3 patterns)
- [FUNCTION_DEFINITIONS](#function-definitions) (3 patterns)
- [OBJECT_OPERATIONS](#object-operations) (4 patterns)
- [REACT_PATTERNS](#react-patterns) (2 patterns)
- [STATE_MANAGEMENT](#state-management) (3 patterns)
- [TEST_PATTERNS](#test-patterns) (7 patterns)

---

## ARRAY_OPERATIONS

*6 patterns, 38,465 total occurrences*

### 58. IDENTIFIER.find

**Statistics:**
- Frequency: 9,312 occurrences
- Prevalence: 74.7% (112 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_SEARCH`

**Examples:**

```javascript
exceptions.find
```
*packages/icalendar/src/ical-expander/IcalExpander.js*

```javascript
$container.find
```
*tests/src/event-render/dayGrid-events.ts*


### 62. IDENTIFIER.forEach

**Statistics:**
- Frequency: 8,991 occurrences
- Prevalence: 81.3% (122 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_ITERATE`

**Examples:**

```javascript
currentDomNodes.forEach
```
*packages/core/src/content-inject/ContentInjector.ts*

```javascript
subs.forEach
```
*packages/core/src/preact.ts*


### 66. IDENTIFIER.filter

**Statistics:**
- Frequency: 8,758 occurrences
- Prevalence: 82.7% (124 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_FILTER`

**Examples:**

```javascript
input.filter
```
*packages/core/src/structs/business-hours.ts*

```javascript
segs.filter
```
*packages/daygrid/src/TableRows.tsx*


### 162. IDENTIFIER.filter(( IDENTIFIER ) => BODY)

**Statistics:**
- Frequency: 4,083 occurrences
- Prevalence: 65.3% (98 repos)
- Node Type: `call_expression`
- Semantic: `IDENTIFIER.ARRAY_FILTER(( IDENTIFIER ) => BODY)`

**Examples:**

```javascript
input.filter((rawDef) => rawDef.daysOfWeek)
```
*packages/core/src/structs/business-hours.ts*

```javascript
filePaths
    .filter((filePath) => (
      // TODO: must proper built dist files (HACK)
      filePath.match(/[\\/]dist[\\/]/)
    ))
```
*scripts/config/karma.js*


### 181. IDENTIFIER.forEach(( IDENTIFIER ) => BODY)

**Statistics:**
- Frequency: 3,667 occurrences
- Prevalence: 64.7% (97 repos)
- Node Type: `call_expression`
- Semantic: `IDENTIFIER.ARRAY_ITERATE(( IDENTIFIER ) => BODY)`

**Examples:**

```javascript
subs.forEach((c) => {
            c.context = _props.value
            c.forceUpdate()
          })
```
*packages/core/src/preact.ts*

```javascript
styleEls.forEach((styleEl) => {
    appendStylesTo(styleEl, styleText)
  })
```
*packages/core/src/styleUtils.ts*


### 182. IDENTIFIER.find(( IDENTIFIER ) => BODY)

**Statistics:**
- Frequency: 3,654 occurrences
- Prevalence: 50.0% (75 repos)
- Node Type: `call_expression`
- Semantic: `IDENTIFIER.ARRAY_SEARCH(( IDENTIFIER ) => BODY)`

**Examples:**

```javascript
llmProviders.find(
      (p) =>
        p.name.toLowerCase() === name.toLowerCase() && p.type.toLowerCase() === type.toLowerCase()
    )
```
*apps/nestjs-backend/src/features/ai/ai.service.ts*

```javascript
llmProviders.find(
      (p) =>
        p.name.toLowerCase() === name.toLowerCase() &&
        p.type.toLowerCase() === type.toLowerCase() &&
        p.models.includes(model)
    )
```
*apps/nestjs-backend/src/features/ai/ai.service.ts*


---

## ASYNC_OPERATIONS

*3 patterns, 14,638 total occurrences*

### 117. IDENTIFIER.resolve

**Statistics:**
- Frequency: 5,586 occurrences
- Prevalence: 60.0% (90 repos)
- Node Type: `member_expression`
- Semantic: `Promise.PROMISE_CREATE`

**Examples:**

```javascript
Promise.resolve
```
*apps/nestjs-backend/src/features/invitation/invitation.service.spec.ts*

```javascript
Promise.resolve
```
*apps/nestjs-backend/src/features/record/typecast.validate.spec.ts*


### 138. IDENTIFIER.resolve

**Statistics:**
- Frequency: 4,698 occurrences
- Prevalence: 75.3% (113 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.PROMISE_CREATE`

**Examples:**

```javascript
require.resolve
```
*bundle/.eslintrc.cjs*

```javascript
require.resolve
```
*packages/bootstrap4/.eslintrc.cjs*


### 147. IDENTIFIER.all

**Statistics:**
- Frequency: 4,354 occurrences
- Prevalence: 70.0% (105 repos)
- Node Type: `member_expression`
- Semantic: `Promise.PROMISE_COMBINE`

**Examples:**

```javascript
Promise.all
```
*scripts/src/archive.ts*

```javascript
Promise.all
```
*scripts/src/archive.ts*


---

## CONTROL_FLOW

*146 patterns, 1,885,204 total occurrences*

### 3. IDENTIFIER(IDENTIFIER)

**Statistics:**
- Frequency: 162,383 occurrences
- Prevalence: 98.7% (148 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
ensureElHasStyles(el)
```
*packages/core/src/Calendar.tsx*

```javascript
memoize(buildViewContext)
```
*packages/core/src/CalendarContent.tsx*


### 4. IDENTIFIER()

**Statistics:**
- Frequency: 128,123 occurrences
- Prevalence: 99.3% (149 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
func()
```
*packages/core/src/Calendar.tsx*

```javascript
createRef<Toolbar>()
```
*packages/core/src/CalendarContent.tsx*


### 5. ( IDENTIFIER ) => BODY

**Statistics:**
- Frequency: 87,739 occurrences
- Prevalence: 89.3% (134 repos)
- Node Type: `arrow_function`

**Examples:**

```javascript
(filename) => filename.replace(/\.ts$/, '')
```
*packages/core/scripts/generate-locales-all.js*

```javascript
(CalendarInteractionClass) => new CalendarInteractionClass(props)
```
*packages/core/src/CalendarContent.tsx*


### 6. IDENTIFIER(IDENTIFIER)

**Statistics:**
- Frequency: 83,765 occurrences
- Prevalence: 76.0% (114 repos)
- Node Type: `call_expression`
- Semantic: `expect(IDENTIFIER)`

**Examples:**

```javascript
expect(selectFired)
```
*tests/src/date-selection/implicit-unselect.ts*

```javascript
expect(unselectFired)
```
*tests/src/date-selection/implicit-unselect.ts*


### 8. IDENTIFIER.length

**Statistics:**
- Frequency: 57,307 occurrences
- Prevalence: 98.0% (147 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
children.length
```
*packages/core/src/ToolbarSection.tsx*

```javascript
viewTypes.length
```
*packages/core/src/api/CalendarImpl.ts*


### 10. IDENTIFIER.id

**Statistics:**
- Frequency: 44,825 occurrences
- Prevalence: 83.3% (125 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
props.id
```
*packages/core/src/common/MorePopover.tsx*

```javascript
props.id
```
*packages/core/src/common/Popover.tsx*


### 11. return IDENTIFIER ;

**Statistics:**
- Frequency: 43,139 occurrences
- Prevalence: 78.0% (117 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return app;
```
*apps/nestjs-backend/src/bootstrap.ts*

```javascript
return port;
```
*apps/nestjs-backend/src/bootstrap.ts*


### 12. IDENTIFIER(IDENTIFIER, IDENTIFIER)

**Statistics:**
- Frequency: 40,357 occurrences
- Prevalence: 94.7% (142 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
parseInteractionSettings(component, settingsInput)
```
*packages/core/src/CalendarContent.tsx*

```javascript
constrainMarkerToRange(currentDate, validRange)
```
*packages/core/src/DateProfileGenerator.ts*


### 13. IDENTIFIER.push

**Statistics:**
- Frequency: 34,203 occurrences
- Prevalence: 94.0% (141 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_MUTATE`

**Examples:**

```javascript
globalPlugins.push
```
*bundle/src/index.ts*

```javascript
globalPlugins.push
```
*packages/bootstrap4/src/index.global.ts*


### 14. IDENTIFIER.name

**Statistics:**
- Frequency: 31,043 occurrences
- Prevalence: 91.3% (137 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
input.name
```
*packages/core/src/plugin-system.ts*

```javascript
def.name
```
*packages/core/src/plugin-system.ts*


### 15. let IDENTIFIER

**Statistics:**
- Frequency: 28,974 occurrences
- Prevalence: 91.3% (137 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
let viewAspectRatio: number | undefined
```
*packages/core/src/CalendarContent.tsx*

```javascript
let validRange: DateRange
```
*packages/core/src/DateProfileGenerator.ts*


### 17. new IDENTIFIER()

**Statistics:**
- Frequency: 28,557 occurrences
- Prevalence: 92.7% (139 repos)
- Node Type: `new_expression`

**Examples:**

```javascript
new TheClass()
```
*packages/core/src/CalendarContent.tsx*

```javascript
new Map<string, CustomRendering<RenderProps>>()
```
*packages/core/src/content-inject/CustomRenderingStore.ts*


### 18. return ;

**Statistics:**
- Frequency: 28,359 occurrences
- Prevalence: 74.7% (112 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return;
```
*apps/nestjs-backend/src/db-provider/filter-query/filter-query.abstract.ts*

```javascript
return;
```
*apps/nestjs-backend/src/event-emitter/event-emitter.service.ts*


### 19. IDENTIFIER.current

**Statistics:**
- Frequency: 27,003 occurrences
- Prevalence: 57.3% (86 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
helpers.current
```
*apps/nextjs-app/src/components/Guide.tsx*

```javascript
helpers.current
```
*apps/nextjs-app/src/components/Guide.tsx*


### 20. const IDENTIFIER = IDENTIFIER()

**Statistics:**
- Frequency: 25,508 occurrences
- Prevalence: 89.3% (134 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const EMPTY_EVENT_STORE = createEmptyEventStore() // for purecomponents. TODO: keep elsewhere
```
*packages/core/src/component/event-splitting.ts*

```javascript
const nonce = getNonceValue()
```
*packages/core/src/styleUtils.ts*


### 21. ( IDENTIFIER , IDENTIFIER ) => BODY

**Statistics:**
- Frequency: 25,146 occurrences
- Prevalence: 95.3% (143 repos)
- Node Type: `arrow_function`

**Examples:**

```javascript
(InnerContent, eventContentArg) => (
          <Fragment>
            <InnerContent
              elTag="div"
              elClasses={['fc-event-main']}
              elStyle={{ color: eventContentAr
```
*packages/core/src/common/StandardEvent.tsx*

```javascript
(obj0, obj1) => compareByFieldSpecs(obj0, obj1, eventOrderSpecs)
```
*packages/core/src/component/event-rendering.ts*


### 22. const IDENTIFIER = ( ) => BODY

**Statistics:**
- Frequency: 24,944 occurrences
- Prevalence: 90.7% (136 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const AuthConfig = () => Inject(authConfig.KEY);
```
*apps/nestjs-backend/src/configs/auth.config.ts*

```javascript
const BaseConfig = () => Inject(baseConfig.KEY);
```
*apps/nestjs-backend/src/configs/base.config.ts*


### 23. IDENTIFIER = IDENTIFIER

**Statistics:**
- Frequency: 24,541 occurrences
- Prevalence: 87.3% (131 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
activeRange = renderRange
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
dateAlignment = unit
```
*packages/core/src/DateProfileGenerator.ts*


### 24. IDENTIFIER(( ) => BODY)

**Statistics:**
- Frequency: 24,001 occurrences
- Prevalence: 82.7% (124 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
flushSync(() => {
        render(
          <CalendarRoot options={currentData.calendarOptions} theme={currentData.theme} emitter={currentData.emitter}>
            {(classNames, height, isHeightAuto,
```
*packages/core/src/Calendar.tsx*

```javascript
flushSync(() => {
      super.updateSize()
    })
```
*packages/core/src/Calendar.tsx*


### 25. IDENTIFIER.type

**Statistics:**
- Frequency: 23,847 occurrences
- Prevalence: 87.3% (131 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
action.type
```
*packages/core/src/Calendar.tsx*

```javascript
viewSpec.type
```
*packages/core/src/CalendarContent.tsx*


### 26. IDENTIFIER.get

**Statistics:**
- Frequency: 23,517 occurrences
- Prevalence: 84.7% (127 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
styleEls.get
```
*packages/core/src/styleUtils.ts*

```javascript
fetchMock.get
```
*tests/src/icalendar/day-view.ts*


### 27. IDENTIFIER.map

**Statistics:**
- Frequency: 22,237 occurrences
- Prevalence: 91.3% (137 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_TRANSFORM`

**Examples:**

```javascript
localeFilenames.map
```
*packages/core/scripts/generate-locales-all.js*

```javascript
interactionClasses.map
```
*packages/core/src/CalendarContent.tsx*


### 28. const IDENTIFIER = IDENTIFIER(IDENTIFIER)

**Statistics:**
- Frequency: 21,960 occurrences
- Prevalence: 93.3% (140 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const touchingEntryId = buildEntryKey(touchingEntry)
```
*packages/daygrid/src/event-placement.ts*

```javascript
const hiddenEntryId = buildEntryKey(hiddenEntry)
```
*packages/daygrid/src/event-placement.ts*


### 29. IDENTIFIER.value

**Statistics:**
- Frequency: 21,252 occurrences
- Prevalence: 83.3% (125 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
_props.value
```
*packages/core/src/preact.ts*

```javascript
_props.value
```
*packages/core/src/preact.ts*


### 31. IDENTIFIER.data

**Statistics:**
- Frequency: 20,091 occurrences
- Prevalence: 73.3% (110 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
job.data
```
*apps/nestjs-backend/src/features/attachments/attachments-crop.processor.ts*

```javascript
job.data
```
*apps/nestjs-backend/src/features/attachments/attachments-crop.processor.ts*


### 32. return BOOLEAN ;

**Statistics:**
- Frequency: 16,741 occurrences
- Prevalence: 70.0% (105 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return true;
```
*packages/icalendar/src/ical-expander/IcalExpander.js*

```javascript
return false;
```
*packages/icalendar/src/ical-expander/IcalExpander.js*


### 33. IDENTIFIER(NUMBER)

**Statistics:**
- Frequency: 16,675 occurrences
- Prevalence: 80.7% (121 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
createContext<number>(0)
```
*packages/core/src/content-inject/RenderId.ts*

```javascript
createDuration(0)
```
*packages/core/src/util/date.ts*


### 34. IDENTIFIER.string

**Statistics:**
- Frequency: 16,533 occurrences
- Prevalence: 50.7% (76 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
Joi.string
```
*apps/nestjs-backend/src/configs/env.validation.schema.ts*

```javascript
Joi.string
```
*apps/nestjs-backend/src/configs/env.validation.schema.ts*


### 35. IDENTIFIER.env

**Statistics:**
- Frequency: 16,082 occurrences
- Prevalence: 80.7% (121 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
process.env
```
*.husky/install.mjs*

```javascript
process.env
```
*.husky/install.mjs*


### 36. IDENTIFIER.join

**Statistics:**
- Frequency: 15,548 occurrences
- Prevalence: 88.0% (132 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_TO_STRING`

**Examples:**

```javascript
classNames.join
```
*packages/core/src/Toolbar.tsx*

```javascript
buttonClasses.join
```
*packages/core/src/ToolbarSection.tsx*


### 37. let IDENTIFIER = NUMBER

**Statistics:**
- Frequency: 15,316 occurrences
- Prevalence: 91.3% (137 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
let runningCount = 0
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
let dayCnt = 0
```
*packages/core/src/DateProfileGenerator.ts*


### 38. IDENTIFIER(BOOLEAN)

**Statistics:**
- Frequency: 15,296 occurrences
- Prevalence: 80.0% (120 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
defineViewTests(false)
```
*tests/src/legacy/event-coloring.ts*

```javascript
defineViewTests(true)
```
*tests/src/legacy/event-coloring.ts*


### 39. IDENTIFIER.includes

**Statistics:**
- Frequency: 14,948 occurrences
- Prevalence: 89.3% (134 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_TEST`

**Examples:**

```javascript
args.includes
```
*scripts/src/clean.ts*

```javascript
args.includes
```
*scripts/src/json.ts*


### 40. IDENTIFIER.string()

**Statistics:**
- Frequency: 14,403 occurrences
- Prevalence: 32.7% (49 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
Joi.string()
```
*apps/nestjs-backend/src/configs/env.validation.schema.ts*

```javascript
Joi.string()
```
*apps/nestjs-backend/src/configs/env.validation.schema.ts*


### 43. const IDENTIFIER = [ ]

**Statistics:**
- Frequency: 11,917 occurrences
- Prevalence: 89.3% (134 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const globalLocales: LocaleInput[] = []
```
*packages/core/src/global-locales.ts*

```javascript
const styleTexts: string[] = []
```
*packages/core/src/styleUtils.ts*


### 44. const IDENTIFIER = new IDENTIFIER()

**Statistics:**
- Frequency: 11,675 occurrences
- Prevalence: 86.7% (130 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const localQueueEventEmitter = new EventEmitter();
```
*apps/nestjs-backend/src/event-emitter/event-job/fallback/event-emitter.ts*

```javascript
const fieldIdSet = new Set<string>();
```
*apps/nestjs-backend/src/event-emitter/listeners/record-history.listener.ts*


### 45. IDENTIFIER.object

**Statistics:**
- Frequency: 11,641 occurrences
- Prevalence: 46.0% (69 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
Joi.object
```
*apps/nestjs-backend/src/configs/env.validation.schema.ts*

```javascript
z.object
```
*apps/nextjs-app/src/features/app/blocks/chart/types.ts*


### 46. IDENTIFIER.message

**Statistics:**
- Frequency: 11,374 occurrences
- Prevalence: 78.0% (117 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
error.message
```
*packages/core/src/reducers/eventSources.ts*

```javascript
error.message
```
*tests/src/legacy/custom-view-duration.ts*


### 47. export default IDENTIFIER ;

**Statistics:**
- Frequency: 11,129 occurrences
- Prevalence: 62.0% (93 repos)
- Node Type: `export_statement`

**Examples:**

```javascript
export default otelSDK;
```
*apps/nestjs-backend/src/tracing.ts*

```javascript
export default WebSocketJSONStream;
```
*apps/nestjs-backend/src/ws/wjs.d.ts*


### 48. return IDENTIFIER

**Statistics:**
- Frequency: 11,088 occurrences
- Prevalence: 34.0% (51 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return code
```
*packages/core/scripts/generate-locale-iife.js*

```javascript
return code
```
*packages/core/scripts/generate-locales-all.js*


### 49. const IDENTIFIER = NUMBER

**Statistics:**
- Frequency: 10,901 occurrences
- Prevalence: 88.7% (133 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const PADDING_FROM_VIEWPORT = 10
```
*packages/core/src/common/Popover.tsx*

```javascript
const AUTO_ALL_DAY_MAX_EVENT_ROWS = 5
```
*packages/timegrid/src/TimeColsView.tsx*


### 51. IDENTIFIER = IDENTIFIER | NUMBER

**Statistics:**
- Frequency: 10,805 occurrences
- Prevalence: 4.0% (6 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
nth = nth | 0
```
*src/vs/base/common/arrays.ts*

```javascript
width = width | 0
```
*src/vs/base/common/scrollable.ts*


### 52. new IDENTIFIER(IDENTIFIER)

**Statistics:**
- Frequency: 10,569 occurrences
- Prevalence: 85.3% (128 repos)
- Node Type: `new_expression`

**Examples:**

```javascript
new CalendarInteractionClass(props)
```
*packages/core/src/CalendarContent.tsx*

```javascript
new TheInteractionClass(settings)
```
*packages/core/src/CalendarContent.tsx*


### 53. return NULL ;

**Statistics:**
- Frequency: 10,411 occurrences
- Prevalence: 63.3% (95 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return null;
```
*apps/nestjs-backend/src/db-provider/search-query/search-index-builder.postgres.ts*

```javascript
return null;
```
*apps/nestjs-backend/src/db-provider/search-query/search-index-builder.postgres.ts*


### 54. IDENTIFIER(IDENTIFIER, IDENTIFIER, IDENTIFIER)

**Statistics:**
- Frequency: 9,957 occurrences
- Prevalence: 84.7% (127 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
buildEventApis(relevantEvents, context, instance)
```
*packages/core/src/api/EventImpl.ts*

```javascript
fabricateEventRange(dateSpan, eventUiBases, context)
```
*packages/core/src/common/slicing-utils.ts*


### 55. IDENTIFIER.set

**Statistics:**
- Frequency: 9,559 occurrences
- Prevalence: 78.7% (118 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
map.set
```
*packages/core/src/content-inject/CustomRenderingStore.ts*

```javascript
styleEls.set
```
*packages/core/src/styleUtils.ts*


### 56. IDENTIFIER.equal

**Statistics:**
- Frequency: 9,541 occurrences
- Prevalence: 18.7% (28 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
assert.equal
```
*config/verifySourceMaps.ts*

```javascript
assert.equal
```
*integration-tests/node/test-cjs.cjs*


### 59. ( IDENTIFIER : STRING ) => BODY

**Statistics:**
- Frequency: 9,274 occurrences
- Prevalence: 89.3% (134 repos)
- Node Type: `arrow_function`

**Examples:**

```javascript
(navUnit: string) => formatWithOrdinals(
              calendarButtonHintOverrides[buttonName] ||
              calendarButtonHints[buttonName],
              [
                calendarButtonText[navU
```
*packages/core/src/toolbar-parse.ts*

```javascript
(cssVarName: string) => {
        return `import { ${inject.importProp} } from ${JSON.stringify(inject.importId)};\n` +
          `injectStyles(${cssVarName});\n`
      }
```
*scripts/src/pkg/utils/rollup-presets.ts*


### 60. export const IDENTIFIER = ( ) => BODY

**Statistics:**
- Frequency: 9,143 occurrences
- Prevalence: 62.7% (94 repos)
- Node Type: `export_statement`

**Examples:**

```javascript
export const AuthConfig = () => Inject(authConfig.KEY);
```
*apps/nestjs-backend/src/configs/auth.config.ts*

```javascript
export const BaseConfig = () => Inject(baseConfig.KEY);
```
*apps/nestjs-backend/src/configs/base.config.ts*


### 61. IDENTIFIER.info

**Statistics:**
- Frequency: 9,125 occurrences
- Prevalence: 48.0% (72 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
logger.info
```
*lib/config/migrate-validate.ts*

```javascript
logger.info
```
*lib/config/presets/index.ts*


### 63. IDENTIFIER.push(IDENTIFIER)

**Statistics:**
- Frequency: 8,975 occurrences
- Prevalence: 84.7% (127 repos)
- Node Type: `call_expression`
- Semantic: `IDENTIFIER.ARRAY_MUTATE(IDENTIFIER)`

**Examples:**

```javascript
globalPlugins.push(plugin)
```
*packages/bootstrap4/src/index.global.ts*

```javascript
globalPlugins.push(plugin)
```
*packages/bootstrap5/src/index.global.ts*


### 64. IDENTIFIER.map(( IDENTIFIER ) => BODY)

**Statistics:**
- Frequency: 8,810 occurrences
- Prevalence: 75.3% (113 repos)
- Node Type: `call_expression`
- Semantic: `IDENTIFIER.ARRAY_TRANSFORM(( IDENTIFIER ) => BODY)`

**Examples:**

```javascript
localeFilenames.map((filename) => filename.replace(/\.ts$/, ''))
```
*packages/core/scripts/generate-locales-all.js*

```javascript
interactionClasses.map((TheInteractionClass) => new TheInteractionClass(settings))
```
*packages/core/src/CalendarContent.tsx*


### 68. IDENTIFIER.status

**Statistics:**
- Frequency: 8,644 occurrences
- Prevalence: 63.3% (95 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
response.status
```
*apps/nestjs-backend/src/features/auth/turnstile/turnstile.service.ts*

```javascript
error.status
```
*apps/nestjs-backend/src/features/oauth/oauth-server.service.ts*


### 70. const IDENTIFIER = IDENTIFIER(IDENTIFIER, IDENTIFIER)

**Statistics:**
- Frequency: 7,938 occurrences
- Prevalence: 76.7% (115 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const keys = getUnequalProps(obj0, obj1)
```
*packages/core/src/util/object.ts*

```javascript
const transpiledDir = joinPaths(pkgDir, transpiledSubdir)
```
*scripts/src/pkg/utils/bundle-struct.ts*


### 71. IDENTIFIER.body

**Statistics:**
- Frequency: 7,918 occurrences
- Prevalence: 51.3% (77 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
fetchOptions.body
```
*packages/core/src/util/requestJson.ts*

```javascript
options.body
```
*tests/src/legacy/events-json-feed.ts*


### 73. IDENTIFIER.slice

**Statistics:**
- Frequency: 7,748 occurrences
- Prevalence: 84.7% (127 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.ARRAY_SLICE`

**Examples:**

```javascript
parts.slice
```
*packages/core/src/datelib/locale.ts*

```javascript
names.slice
```
*scripts/src/pkg/bundle.ts*


### 74. IDENTIFIER.children

**Statistics:**
- Frequency: 7,705 occurrences
- Prevalence: 58.0% (87 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
props.children
```
*packages/core/src/CalendarRoot.tsx*

```javascript
props.children
```
*packages/core/src/NowTimer.ts*


### 75. IDENTIFIER.exports

**Statistics:**
- Frequency: 7,657 occurrences
- Prevalence: 71.3% (107 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
module.exports
```
*bundle/.eslintrc.cjs*

```javascript
module.exports
```
*packages/bootstrap4/.eslintrc.cjs*


### 76. IDENTIFIER.key

**Statistics:**
- Frequency: 7,545 occurrences
- Prevalence: 71.3% (107 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
ev.key
```
*packages/core/src/common/Popover.tsx*

```javascript
sectionConfig.key
```
*packages/core/src/scrollgrid/SimpleScrollGrid.tsx*


### 77. return

**Statistics:**
- Frequency: 7,328 occurrences
- Prevalence: 32.0% (48 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return
```
*packages/core/src/api/EventImpl.ts*

```javascript
return
```
*packages/core/src/option-change-handlers.ts*


### 81. IDENTIFIER.content

**Statistics:**
- Frequency: 7,077 occurrences
- Prevalence: 53.3% (80 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
chunkConfig.content
```
*packages/core/src/scrollgrid/util.tsx*

```javascript
chunkConfig.content
```
*packages/core/src/scrollgrid/util.tsx*


### 82. IDENTIFIER(IDENTIFIER).not

**Statistics:**
- Frequency: 7,006 occurrences
- Prevalence: 51.3% (77 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER).not`

**Examples:**

```javascript
expect(smallEventCnt).not
```
*tests/src/event-render/dayGrid-events.ts*

```javascript
expect(eventEl).not
```
*tests/src/legacy/DayGrid-events.ts*


### 83. IDENTIFIER = NUMBER

**Statistics:**
- Frequency: 6,996 occurrences
- Prevalence: 66.0% (99 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
i = 0
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
i = 0
```
*packages/core/src/api/CalendarImpl.ts*


### 87. IDENTIFIER.t

**Statistics:**
- Frequency: 6,658 occurrences
- Prevalence: 11.3% (17 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
color.t
```
*packages/react/src/components/ColorPicker/ColorPicker.base.tsx*

```javascript
textLabels.t
```
*packages/react/src/components/ColorPicker/ColorPicker.base.tsx*


### 89. IDENTIFIER.replace

**Statistics:**
- Frequency: 6,609 occurrences
- Prevalence: 80.0% (120 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
filename.replace
```
*packages/core/scripts/generate-locales-all.js*

```javascript
s.replace
```
*packages/core/src/datelib/formatting-native.ts*


### 92. IDENTIFIER(IDENTIFIER).toHaveBeenCalledTimes

**Statistics:**
- Frequency: 6,431 occurrences
- Prevalence: 37.3% (56 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER).toHaveBeenCalledTimes`

**Examples:**

```javascript
expect(sendTransactionSpy).toHaveBeenCalledTimes
```
*packages/web3/test/integration/contract-middleware.test.ts*

```javascript
expect(getterSpy).toHaveBeenCalledTimes
```
*packages/web3-core/test/unit/web3_config.test.ts*


### 93. IDENTIFIER.url

**Statistics:**
- Frequency: 6,430 occurrences
- Prevalence: 65.3% (98 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
def.url
```
*packages/core/src/api/EventImpl.ts*

```javascript
def.url
```
*packages/core/src/api/EventImpl.ts*


### 94. IDENTIFIER(( ) => BODY)

**Statistics:**
- Frequency: 6,373 occurrences
- Prevalence: 60.0% (90 repos)
- Node Type: `call_expression`
- Semantic: `beforeEach(( ) => BODY)`

**Examples:**

```javascript
beforeEach(() => {
    enLocale = new Calendar(document.createElement('div'), { // HACK
      plugins: [dayGridPlugin],
    }).getCurrentData().dateEnv.locale
  })
```
*tests/src/datelib/main.ts*

```javascript
beforeEach(() => {
      env = new DateEnv({
        timeZone: 'UTC',
        calendarSystem: 'gregory',
        locale: enLocale,
      })
    })
```
*tests/src/datelib/main.ts*


### 95. IDENTIFIER = IDENTIFIER + NUMBER | NUMBER

**Statistics:**
- Frequency: 6,355 occurrences
- Prevalence: 2.7% (4 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
n=e+44|0
```
*.yarn/plugins/@yarnpkg/plugin-interactive-tools.cjs*

```javascript
e=e+4|0
```
*.yarn/plugins/@yarnpkg/plugin-interactive-tools.cjs*


### 96. IDENTIFIER(IDENTIFIER).toHaveBeenCalledTimes(NUMBER)

**Statistics:**
- Frequency: 6,348 occurrences
- Prevalence: 37.3% (56 repos)
- Node Type: `call_expression`
- Semantic: `expect(IDENTIFIER).toHaveBeenCalledTimes(NUMBER)`

**Examples:**

```javascript
expect(sendTransactionSpy).toHaveBeenCalledTimes(1)
```
*packages/web3/test/integration/contract-middleware.test.ts*

```javascript
expect(getterSpy).toHaveBeenCalledTimes(1)
```
*packages/web3-core/test/unit/web3_config.test.ts*


### 98. IDENTIFIER.text

**Statistics:**
- Frequency: 6,257 occurrences
- Prevalence: 69.3% (104 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
props.text
```
*packages/core/src/common/MoreLinkContainer.tsx*

```javascript
innerProps.text
```
*packages/core/src/common/WeekNumberContainer.tsx*


### 99. IDENTIFIER = BOOLEAN

**Statistics:**
- Frequency: 6,227 occurrences
- Prevalence: 82.0% (123 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
viewVGrow = true
```
*packages/core/src/CalendarContent.tsx*

```javascript
forceLtr = true
```
*packages/core/src/Toolbar.tsx*


### 100. IDENTIFIER.add

**Statistics:**
- Frequency: 6,204 occurrences
- Prevalence: 66.7% (100 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
classList.add
```
*packages/core/src/Calendar.tsx*

```javascript
dateEnv.add
```
*packages/core/src/DateProfileGenerator.ts*


### 101. IDENTIFIER.target

**Statistics:**
- Frequency: 6,102 occurrences
- Prevalence: 63.3% (95 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
ev.target
```
*packages/core/src/CalendarContent.tsx*

```javascript
ev.target
```
*packages/core/src/component/event-rendering.ts*


### 102. IDENTIFIER.shape

**Statistics:**
- Frequency: 6,096 occurrences
- Prevalence: 15.3% (23 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
oauthCreateRoSchema.shape
```
*apps/nextjs-app/src/features/app/blocks/setting/oauth-app/manage/OAuthAppForm.tsx*

```javascript
oauthCreateRoSchema.shape
```
*apps/nextjs-app/src/features/app/blocks/setting/oauth-app/manage/OAuthAppForm.tsx*


### 103. IDENTIFIER.default

**Statistics:**
- Frequency: 6,067 occurrences
- Prevalence: 48.0% (72 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
suites.default
```
*scripts/src/pkg/test.ts*

```javascript
generatorExports.default
```
*scripts/src/pkg/utils/bundle-struct.ts*


### 107. IDENTIFIER = IDENTIFIER [ IDENTIFIER >> NUMBER ] | NUMBER

**Statistics:**
- Frequency: 5,881 occurrences
- Prevalence: 2.7% (4 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
r=t[n>>2]|0
```
*.yarn/plugins/@yarnpkg/plugin-interactive-tools.cjs*

```javascript
o=t[r>>2]|0
```
*.yarn/plugins/@yarnpkg/plugin-interactive-tools.cjs*


### 108. IDENTIFIER.title

**Statistics:**
- Frequency: 5,857 occurrences
- Prevalence: 63.3% (95 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
props.title
```
*packages/core/src/Toolbar.tsx*

```javascript
props.title
```
*packages/core/src/ToolbarSection.tsx*


### 109. IDENTIFIER.on

**Statistics:**
- Frequency: 5,849 occurrences
- Prevalence: 66.0% (99 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
emitter.on
```
*packages/core/src/CalendarRoot.tsx*

```javascript
emitter.on
```
*packages/core/src/CalendarRoot.tsx*


### 111. IDENTIFIER.map(() => BODY)

**Statistics:**
- Frequency: 5,780 occurrences
- Prevalence: 38.0% (57 repos)
- Node Type: `call_expression`
- Semantic: `IDENTIFIER.ARRAY_TRANSFORM(() => BODY)`

**Examples:**

```javascript
packages.map(p => `packages/${p}`)
```
*docs/docusaurus.config.js*

```javascript
keys.map(num => numberToHex(num))
```
*packages/web3-core/src/formatters.ts*


### 113. IDENTIFIER.editor

**Statistics:**
- Frequency: 5,705 occurrences
- Prevalence: 16.0% (24 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
opBuilder?.editor
```
*apps/nestjs-backend/src/event-emitter/event-emitter.service.ts*

```javascript
RecordOpBuilder.editor
```
*apps/nestjs-backend/src/features/calculation/batch.service.ts*


### 114. IDENTIFIER.has

**Statistics:**
- Frequency: 5,674 occurrences
- Prevalence: 69.3% (104 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
SELECT_FIELD_TYPE_SET.has
```
*apps/nestjs-backend/src/event-emitter/listeners/record-history.listener.ts*

```javascript
valueSet.has
```
*apps/nestjs-backend/src/event-emitter/listeners/record-history.listener.ts*


### 116. IDENTIFIER.getByRole

**Statistics:**
- Frequency: 5,610 occurrences
- Prevalence: 16.7% (25 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
screen.getByRole
```
*apps/nextjs-app/src/components/layout/__tests__/MainLayout.test.tsx*

```javascript
screen.getByRole
```
*packages/sdk/src/components/filter/view-filter/component/base/__tests__/BaseMultipleSelect.test.tsx*


### 118. IDENTIFIER.strictEqual

**Statistics:**
- Frequency: 5,528 occurrences
- Prevalence: 13.3% (20 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
assert.strictEqual
```
*config/version.ts*

```javascript
assert.strictEqual
```
*config/version.ts*


### 119. const IDENTIFIER = IDENTIFIER [ IDENTIFIER ]

**Statistics:**
- Frequency: 5,495 occurrences
- Prevalence: 82.7% (124 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const severity = EXTENDED_SETTINGS_AND_SEVERITIES[name]
```
*packages/core/src/datelib/formatting-native.ts*

```javascript
const currentId = currentPluginIds[pluginName]
```
*packages/core/src/plugin-system.ts*


### 120. IDENTIFIER.number

**Statistics:**
- Frequency: 5,483 occurrences
- Prevalence: 42.7% (64 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
Joi.number
```
*apps/nestjs-backend/src/configs/env.validation.schema.ts*

```javascript
faker.number
```
*apps/nestjs-backend/src/features/selection/selection.service.spec.ts*


### 121. const IDENTIFIER = ( IDENTIFIER : STRING ) => BODY

**Statistics:**
- Frequency: 5,446 occurrences
- Prevalence: 75.3% (113 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const createLocalQueueProvider = (queueName: string): Provider => ({
  provide: getQueueToken(queueName),
  useFactory: async () => {
    return {
      add: (name: string, data: unknown, opts?: JobsO
```
*apps/nestjs-backend/src/event-emitter/event-job/fallback/local-queue.provider.ts*

```javascript
const splitAccessToken = (accessToken: string) => {
  const [prefix = '', accessTokenId = '', encryptedSign = ''] = accessToken.split('_');
  if (!accessTokenId) {
    return null;
  }
  if (prefix !=
```
*apps/nestjs-backend/src/features/access-token/access-token.encryptor.ts*


### 122. ( IDENTIFIER : any ) => BODY

**Statistics:**
- Frequency: 5,384 occurrences
- Prevalence: 66.7% (100 repos)
- Node Type: `arrow_function`

**Examples:**

```javascript
(statement: any) => statement.grouping === 'group'
```
*apps/nestjs-backend/src/features/base/base-query/parse/select.ts*

```javascript
(statement: any) => statement.value
```
*apps/nestjs-backend/src/features/base/base-query/parse/select.ts*


### 123. IDENTIFIER.split

**Statistics:**
- Frequency: 5,349 occurrences
- Prevalence: 84.0% (126 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
styleText.split
```
*packages/core/src/styleUtils.ts*

```javascript
sectionStr.split
```
*packages/core/src/toolbar-parse.ts*


### 124. IDENTIFIER.displayName

**Statistics:**
- Frequency: 5,217 occurrences
- Prevalence: 40.7% (61 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
SvgrMock.displayName
```
*apps/nextjs-app/config/tests/ReactSvgrMock.tsx*

```javascript
WorkFlowPanel.displayName
```
*apps/nextjs-app/src/features/app/automation/workflow-panel/WorkFlowPanel.tsx*


### 125. IDENTIFIER.prototype

**Statistics:**
- Frequency: 5,123 occurrences
- Prevalence: 52.7% (79 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
BootstrapTheme.prototype
```
*packages/bootstrap4/src/BootstrapTheme.ts*

```javascript
BootstrapTheme.prototype
```
*packages/bootstrap4/src/BootstrapTheme.ts*


### 127. IDENTIFIER.debug

**Statistics:**
- Frequency: 5,089 occurrences
- Prevalence: 38.0% (57 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
options.debug
```
*tests/src/lib/simulate.ts*

```javascript
options.debug
```
*tests/src/lib/simulate.ts*


### 128. IDENTIFIER.toString

**Statistics:**
- Frequency: 5,078 occurrences
- Prevalence: 80.0% (120 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
warning.toString
```
*scripts/src/pkg/utils/rollup-presets.ts*

```javascript
actual.toString
```
*tests/src/lib/date-matchers.ts*


### 129. const IDENTIFIER = { }

**Statistics:**
- Frequency: 5,075 occurrences
- Prevalence: 78.0% (117 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const interactionSettingsStore: InteractionSettingsStore = {}
```
*packages/core/src/interactions/interaction.ts*

```javascript
const defIdMap: EventDefIdMap = {}
```
*packages/core/src/reducers/eventStore.ts*


### 130. IDENTIFIER.isArray(IDENTIFIER)

**Statistics:**
- Frequency: 5,035 occurrences
- Prevalence: 77.3% (116 repos)
- Node Type: `call_expression`
- Semantic: `Array.isArray(IDENTIFIER)`

**Examples:**

```javascript
Array.isArray(input)
```
*packages/core/src/datelib/env.ts*

```javascript
Array.isArray(inputSingular)
```
*packages/core/src/datelib/locale.ts*


### 133. IDENTIFIER.deepEqual

**Statistics:**
- Frequency: 4,946 occurrences
- Prevalence: 14.7% (22 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
assert.deepEqual
```
*addons/addon-image/src/IIPHeaderParser.test.ts*

```javascript
assert.deepEqual
```
*addons/addon-image/src/IIPHeaderParser.test.ts*


### 134. IDENTIFIER(IDENTIFIER.length)

**Statistics:**
- Frequency: 4,903 occurrences
- Prevalence: 48.7% (73 repos)
- Node Type: `call_expression`
- Semantic: `expect(IDENTIFIER.length)`

**Examples:**

```javascript
expect(events.length)
```
*tests/src/datelib/rrule.ts*

```javascript
expect(events.length)
```
*tests/src/datelib/rrule.ts*


### 135. const IDENTIFIER

**Statistics:**
- Frequency: 4,855 occurrences
- Prevalence: 44.0% (66 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const module: any;
```
*apps/nestjs-backend/src/bootstrap.ts*

```javascript
const svg: React.VFC<React.SVGProps<SVGSVGElement>>;
```
*apps/nextjs-app/src/types.d/react-svgr.d.ts*


### 137. IDENTIFIER.getByLabel

**Statistics:**
- Frequency: 4,757 occurrences
- Prevalence: 5.3% (8 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
element.getByLabel
```
*packages/charts/chart-web-components/src/donut-chart/donut-chart.spec.ts*

```javascript
element.getByLabel
```
*packages/charts/chart-web-components/src/donut-chart/donut-chart.spec.ts*


### 139. let IDENTIFIER = BOOLEAN

**Statistics:**
- Frequency: 4,667 occurrences
- Prevalence: 80.7% (121 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
let viewVGrow = false
```
*packages/core/src/CalendarContent.tsx*

```javascript
let forceLtr = false
```
*packages/core/src/Toolbar.tsx*


### 140. IDENTIFIER.path

**Statistics:**
- Frequency: 4,609 occurrences
- Prevalence: 62.7% (94 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
file.path
```
*apps/nestjs-backend/src/features/attachments/attachments.service.ts*

```javascript
file.path
```
*apps/nestjs-backend/src/features/attachments/attachments.service.ts*


### 141. IDENTIFIER [ IDENTIFIER >> NUMBER ] = IDENTIFIER

**Statistics:**
- Frequency: 4,489 occurrences
- Prevalence: 3.3% (5 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
HEAP32[DYNAMICTOP_PTR>>2]=f
```
*.yarn/plugins/@yarnpkg/plugin-interactive-tools.cjs*

```javascript
HEAP32[DYNAMICTOP_PTR>>2]=u
```
*.yarn/plugins/@yarnpkg/plugin-interactive-tools.cjs*


### 142. IDENTIFIER(IDENTIFIER [ NUMBER ])

**Statistics:**
- Frequency: 4,472 occurrences
- Prevalence: 43.3% (65 repos)
- Node Type: `call_expression`
- Semantic: `expect(IDENTIFIER [ NUMBER ])`

**Examples:**

```javascript
expect(timeTexts[0])
```
*tests/src/datelib/moment.ts*

```javascript
expect(timeTexts[0])
```
*tests/src/datelib/rrule.ts*


### 143. IDENTIFIER.element

**Statistics:**
- Frequency: 4,434 occurrences
- Prevalence: 23.3% (35 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
props.element
```
*packages/sdk/src/components/plate/ui/image-element.tsx*

```javascript
props.element
```
*packages/sdk/src/components/plate/ui/link-element.tsx*


### 144. IDENTIFIER.config

**Statistics:**
- Frequency: 4,423 occurrences
- Prevalence: 53.3% (80 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
aiIntegration?.config
```
*apps/nestjs-backend/src/features/ai/ai.service.ts*

```javascript
aiIntegration.config
```
*apps/nestjs-backend/src/features/ai/ai.service.ts*


### 145. IDENTIFIER.from

**Statistics:**
- Frequency: 4,414 occurrences
- Prevalence: 62.7% (94 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
qb.from
```
*apps/nestjs-backend/src/db-provider/search-query/search-query.postgres.ts*

```javascript
qb.from
```
*apps/nestjs-backend/src/db-provider/search-query/search-query.postgres.ts*


### 148. IDENTIFIER(( IDENTIFIER ) => BODY)

**Statistics:**
- Frequency: 4,329 occurrences
- Prevalence: 50.0% (75 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
continuousAsync(async (rerun) => {
    const monorepoStruct = initialMonorepoStruct || (await readMonorepo(monorepoDir))
    initialMonorepoStruct = undefined

    const relevantPaths = getMonorepoRel
```
*scripts/src/utils/monorepo-struct.ts*

```javascript
describeTimeZones((tz) => {
    describe('in month view', () => {
      pushOptions({
        initialView: 'dayGridMonth',
      })

      it('moves to day', () => {
        let dateClickSpy = spyOnCa
```
*tests/src/legacy/navLinks.ts*


### 149. IDENTIFIER.toString()

**Statistics:**
- Frequency: 4,322 occurrences
- Prevalence: 78.7% (118 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
warning.toString()
```
*scripts/src/pkg/utils/rollup-presets.ts*

```javascript
actual.toString()
```
*tests/src/lib/date-matchers.ts*


### 150. IDENTIFIER.start

**Statistics:**
- Frequency: 4,297 occurrences
- Prevalence: 54.7% (82 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
renderRange.start
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
range.start
```
*packages/core/src/DateProfileGenerator.ts*


### 151. IDENTIFIER.startsWith

**Statistics:**
- Frequency: 4,287 occurrences
- Prevalence: 76.0% (114 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
arg.startsWith
```
*scripts/src/pkg/test.ts*

```javascript
globalName.startsWith
```
*scripts/src/pkg/utils/bundle-struct.ts*


### 152. IDENTIFIER.create

**Statistics:**
- Frequency: 4,275 occurrences
- Prevalence: 53.3% (80 repos)
- Node Type: `member_expression`
- Semantic: `IDENTIFIER.OBJECT_CREATE`

**Examples:**

```javascript
refined.create
```
*packages/core/src/structs/drag-meta.ts*

```javascript
refined.create
```
*packages/core/src/structs/drag-meta.ts*


### 153. ( IDENTIFIER , IDENTIFIER , IDENTIFIER ) => BODY

**Statistics:**
- Frequency: 4,271 occurrences
- Prevalence: 72.0% (108 repos)
- Node Type: `arrow_function`

**Examples:**

```javascript
(InnerContent, renderProps, elAttrs) => (
          <Popover
            elRef={elAttrs.ref}
            id={props.id}
            title={title}
            extraClassNames={
              ['fc-more-p
```
*packages/core/src/common/MorePopover.tsx*

```javascript
(str, arg, index) => (
      str.replace('$' + index, arg || '')
    )
```
*packages/core/src/util/misc.ts*


### 154. IDENTIFIER.get(IDENTIFIER)

**Statistics:**
- Frequency: 4,271 occurrences
- Prevalence: 69.3% (104 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
app.get(ConfigService)
```
*apps/nestjs-backend/src/bootstrap.ts*

```javascript
app.get(Logger)
```
*apps/nestjs-backend/src/bootstrap.ts*


### 155. IDENTIFIER.click

**Statistics:**
- Frequency: 4,266 occurrences
- Prevalence: 42.0% (63 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
customButtonProps.click
```
*packages/core/src/toolbar-parse.ts*

```javascript
customButtonProps.click
```
*packages/core/src/toolbar-parse.ts*


### 156. IDENTIFIER(IDENTIFIER, NUMBER)

**Statistics:**
- Frequency: 4,235 occurrences
- Prevalence: 72.0% (108 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
addDays(end, 1)
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
addDays(start, 1)
```
*packages/core/src/NowTimer.ts*


### 158. IDENTIFIER.width

**Statistics:**
- Frequency: 4,214 occurrences
- Prevalence: 60.0% (90 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
popoverDims.width
```
*packages/core/src/common/Popover.tsx*

```javascript
popoverDims.width
```
*packages/core/src/common/Popover.tsx*


### 159. const IDENTIFIER = new IDENTIFIER(IDENTIFIER)

**Statistics:**
- Frequency: 4,172 occurrences
- Prevalence: 68.7% (103 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const viewWrapper = new MultiMonthViewWrapper(calendar)
```
*tests/src/event-render/multiMonth-events.ts*

```javascript
const elListenerCounter = new ListenerCounter(el)
```
*tests/src/lib/vdom-misc.ts*


### 161. IDENTIFIER.options

**Statistics:**
- Frequency: 4,156 occurrences
- Prevalence: 54.0% (81 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
props.options
```
*packages/core/src/CalendarContent.tsx*

```javascript
context.options
```
*packages/core/src/NowTimer.ts*


### 163. IDENTIFIER.node

**Statistics:**
- Frequency: 4,041 occurrences
- Prevalence: 38.7% (58 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
globals.node
```
*eslint.config.mjs*

```javascript
globals.node
```
*eslint.config.mjs*


### 166. IDENTIFIER.headers

**Statistics:**
- Frequency: 4,000 occurrences
- Prevalence: 42.0% (63 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
headResponse.headers
```
*apps/nestjs-backend/src/features/attachments/attachments.service.ts*

```javascript
headResponse.headers
```
*apps/nestjs-backend/src/features/attachments/attachments.service.ts*


### 167. IDENTIFIER.height

**Statistics:**
- Frequency: 3,970 occurrences
- Prevalence: 56.0% (84 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
options.height
```
*packages/core/src/CalendarContent.tsx*

```javascript
options.height
```
*packages/core/src/CalendarRoot.tsx*


### 168. return BOOLEAN

**Statistics:**
- Frequency: 3,932 occurrences
- Prevalence: 26.0% (39 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return false
```
*packages/core/src/common/PositionCache.ts*

```javascript
return false
```
*packages/core/src/common/PositionCache.ts*


### 169. IDENTIFIER.metadata

**Statistics:**
- Frequency: 3,928 occurrences
- Prevalence: 28.7% (43 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
image.metadata
```
*apps/nestjs-backend/src/features/attachments/plugins/local.ts*

```javascript
sharpReader.metadata
```
*apps/nestjs-backend/src/features/attachments/plugins/minio.ts*


### 170. IDENTIFIER(IDENTIFIER).toHaveAttribute

**Statistics:**
- Frequency: 3,921 occurrences
- Prevalence: 8.0% (12 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER).toHaveAttribute`

**Examples:**

```javascript
expect(todo).toHaveAttribute
```
*src/react/hooks/__tests__/useLoadableQuery.test.tsx*

```javascript
expect(todo).toHaveAttribute
```
*src/react/hooks/__tests__/useLoadableQuery.test.tsx*


### 171. IDENTIFIER.preventDefault

**Statistics:**
- Frequency: 3,917 occurrences
- Prevalence: 57.3% (86 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
ev.preventDefault
```
*packages/core/src/util/dom-event.ts*

```javascript
ev.preventDefault
```
*packages/core/src/util/dom-event.ts*


### 172. return IDENTIFIER(IDENTIFIER) ;

**Statistics:**
- Frequency: 3,917 occurrences
- Prevalence: 59.3% (89 repos)
- Node Type: `return_statement`

**Examples:**

```javascript
return chosenHandler(builderClient);
```
*apps/nestjs-backend/src/db-provider/sort-query/function/sort-function.abstract.ts*

```javascript
return convertValueToStringify(groupByValue);
```
*apps/nestjs-backend/src/features/aggregation/aggregation.service.ts*


### 174. IDENTIFIER.success

**Statistics:**
- Frequency: 3,861 occurrences
- Prevalence: 40.7% (61 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
eventSource.success
```
*packages/core/src/reducers/eventSources.ts*

```javascript
eventSource.success
```
*packages/core/src/reducers/eventSources.ts*


### 175. IDENTIFIER.close

**Statistics:**
- Frequency: 3,851 occurrences
- Prevalence: 54.7% (82 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
rollupWatcher.close
```
*scripts/src/pkg/bundle.ts*

```javascript
fileWatcher.close
```
*scripts/src/pkg/bundle.ts*


### 176. IDENTIFIER.preventDefault()

**Statistics:**
- Frequency: 3,827 occurrences
- Prevalence: 57.3% (86 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
ev.preventDefault()
```
*packages/core/src/util/dom-event.ts*

```javascript
ev.preventDefault()
```
*packages/core/src/util/dom-event.ts*


### 177. IDENTIFIER.warn

**Statistics:**
- Frequency: 3,792 occurrences
- Prevalence: 38.0% (57 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
logger.warn
```
*lib/config/decrypt/openpgp.spec.ts*

```javascript
logger.warn
```
*lib/config/decrypt/openpgp.ts*


### 178. IDENTIFIER = IDENTIFIER(IDENTIFIER)

**Statistics:**
- Frequency: 3,790 occurrences
- Prevalence: 66.7% (100 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
start = startOfDay(start)
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
end = startOfDay(end)
```
*packages/core/src/DateProfileGenerator.ts*


### 179. let IDENTIFIER = IDENTIFIER

**Statistics:**
- Frequency: 3,744 occurrences
- Prevalence: 79.3% (119 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
let start: DateMarker = date
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
let end = marker
```
*packages/core/src/calendar-utils.ts*


### 180. IDENTIFIER.query

**Statistics:**
- Frequency: 3,721 occurrences
- Prevalence: 36.7% (55 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
storage?.query
```
*apps/nestjs-backend/src/features/plugin/official/chart/plugin-chart.service.ts*

```javascript
storage?.query
```
*apps/nestjs-backend/src/features/plugin/official/chart/plugin-chart.service.ts*


### 183. IDENTIFIER.number()

**Statistics:**
- Frequency: 3,643 occurrences
- Prevalence: 20.0% (30 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
Joi.number()
```
*apps/nestjs-backend/src/configs/env.validation.schema.ts*

```javascript
z.number()
```
*apps/nextjs-app/src/features/app/blocks/chart/types.ts*


### 184. IDENTIFIER.match

**Statistics:**
- Frequency: 3,642 occurrences
- Prevalence: 64.7% (97 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
cmdStr.match
```
*packages/luxon1/src/format.ts*

```javascript
cmdStr.match
```
*packages/luxon2/src/format.ts*


### 186. IDENTIFIER.any(IDENTIFIER)

**Statistics:**
- Frequency: 3,612 occurrences
- Prevalence: 30.7% (46 repos)
- Node Type: `call_expression`
- Semantic: `expect.any(IDENTIFIER)`

**Examples:**

```javascript
expect.any(String)
```
*apps/nestjs-backend/src/features/access-token/access-token.service.spec.ts*

```javascript
expect.any(Number)
```
*apps/nestjs-backend/src/features/auth/session/session-store.service.spec.ts*


### 187. const IDENTIFIER = ( IDENTIFIER ) => BODY

**Statistics:**
- Frequency: 3,572 occurrences
- Prevalence: 51.3% (77 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const AppProviders: FC<Props & { env: IServerEnv }> = (props) => {
  const { children, env } = props;
  const { query } = useRouter();
  const theme = query.theme as string;

  return (
    <ThemeProv
```
*apps/nextjs-app/src/AppProviders.tsx*

```javascript
const Selector: React.FC<ISelectorProps> = (props) => {
  const { t } = useTranslation('common');
  const {
    onChange,
    readonly,
    selectedId = '',
    placeholder,
    searchTip = t('actions
```
*apps/nextjs-app/src/components/Selector.tsx*


### 191. IDENTIFIER.trim

**Statistics:**
- Frequency: 3,475 occurrences
- Prevalence: 66.0% (99 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
s.trim
```
*packages/core/src/datelib/formatting-native.ts*

```javascript
styleStr.trim
```
*packages/core/src/styleUtils.ts*


### 192. IDENTIFIER(NULL)

**Statistics:**
- Frequency: 3,470 occurrences
- Prevalence: 60.0% (90 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
isLinkCellValue(null)
```
*apps/nestjs-backend/src/features/calculation/utils/detect-link.spec.ts*

```javascript
callback(null)
```
*apps/nestjs-backend/src/share-db/sharedb-redis.pubsub.ts*


### 193. const IDENTIFIER = IDENTIFIER

**Statistics:**
- Frequency: 3,469 occurrences
- Prevalence: 79.3% (119 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const recordIds = result;
```
*apps/nestjs-backend/src/features/aggregation/aggregation.service.ts*

```javascript
const objectName = path;
```
*apps/nestjs-backend/src/features/attachments/plugins/minio.ts*


### 194. IDENTIFIER(IDENTIFIER).to

**Statistics:**
- Frequency: 3,439 occurrences
- Prevalence: 11.3% (17 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER).to`

**Examples:**

```javascript
expect(opacity).to
```
*packages/react-components/react-drawer/library/src/components/DrawerFooter/DrawerFooter.cy.tsx*

```javascript
expect(opacity).to
```
*packages/react-components/react-drawer/library/src/components/DrawerHeader/DrawerHeader.cy.tsx*


### 195. IDENTIFIER(IDENTIFIER).toBeDefined

**Statistics:**
- Frequency: 3,434 occurrences
- Prevalence: 36.0% (54 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER).toBeDefined`

**Examples:**

```javascript
expect(configService).toBeDefined
```
*apps/nestjs-backend/src/configs/config.spec.ts*

```javascript
expect(controller).toBeDefined
```
*apps/nestjs-backend/src/features/access-token/access-token.controller.spec.ts*


### 196. IDENTIFIER(IDENTIFIER).toBeDefined()

**Statistics:**
- Frequency: 3,434 occurrences
- Prevalence: 36.0% (54 repos)
- Node Type: `call_expression`
- Semantic: `expect(IDENTIFIER).toBeDefined()`

**Examples:**

```javascript
expect(configService).toBeDefined()
```
*apps/nestjs-backend/src/configs/config.spec.ts*

```javascript
expect(controller).toBeDefined()
```
*apps/nestjs-backend/src/features/access-token/access-token.controller.spec.ts*


### 198. IDENTIFIER.indexOf

**Statistics:**
- Frequency: 3,385 occurrences
- Prevalence: 73.3% (110 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
hiddenDays.indexOf
```
*packages/core/src/DateProfileGenerator.ts*

```javascript
full0.indexOf
```
*packages/core/src/datelib/formatting-native.ts*


### 199. IDENTIFIER.trim()

**Statistics:**
- Frequency: 3,362 occurrences
- Prevalence: 66.0% (99 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
s.trim()
```
*packages/core/src/datelib/formatting-native.ts*

```javascript
styleStr.trim()
```
*packages/core/src/styleUtils.ts*


### 200. IDENTIFIER.includes(IDENTIFIER)

**Statistics:**
- Frequency: 3,357 occurrences
- Prevalence: 68.0% (102 repos)
- Node Type: `call_expression`
- Semantic: `IDENTIFIER.ARRAY_TEST(IDENTIFIER)`

**Examples:**

```javascript
ignoreMcvFunc.includes(aggFunc)
```
*apps/nestjs-backend/src/db-provider/aggregation-query/aggregation-function.abstract.ts*

```javascript
validStatisticFunc.includes(statisticFunc)
```
*apps/nestjs-backend/src/db-provider/aggregation-query/aggregation-query.abstract.ts*


---

## DATA_FETCHING

*9 patterns, 415,116 total occurrences*

### 2. await EXPRESSION

**Statistics:**
- Frequency: 287,550 occurrences
- Prevalence: 96.0% (144 repos)
- Node Type: `await_expression`

**Examples:**

```javascript
await readFile(templatePath, 'utf8')
```
*packages/core/scripts/generate-locale-iife.js*

```javascript
await globby('*.ts', { cwd: localesDir })
```
*packages/core/scripts/generate-locales-all.js*


### 7. const IDENTIFIER = await EXPRESSION

**Statistics:**
- Frequency: 77,445 occurrences
- Prevalence: 91.3% (137 repos)
- Node Type: `lexical_declaration`

**Examples:**

```javascript
const templateText = await readFile(templatePath, 'utf8')
```
*packages/core/scripts/generate-locale-iife.js*

```javascript
const localeFilenames = await globby('*.ts', { cwd: localesDir })
```
*packages/core/scripts/generate-locales-all.js*


### 41. IDENTIFIER.stringify

**Statistics:**
- Frequency: 13,818 occurrences
- Prevalence: 89.3% (134 repos)
- Node Type: `member_expression`
- Semantic: `JSON.stringify`

**Examples:**

```javascript
JSON.stringify
```
*packages/core/src/structs/view-spec.ts*

```javascript
JSON.stringify
```
*scripts/src/pkg/utils/rollup-presets.ts*


### 85. IDENTIFIER.parse

**Statistics:**
- Frequency: 6,843 occurrences
- Prevalence: 80.0% (120 repos)
- Node Type: `member_expression`
- Semantic: `JSON.parse`

**Examples:**

```javascript
JSON.parse
```
*packages/interaction/src/interactions-external/ExternalElementDragging.ts*

```javascript
JSON.parse
```
*packages/web-component/src/FullCalendarElement.ts*


### 86. IDENTIFIER = await EXPRESSION

**Statistics:**
- Frequency: 6,689 occurrences
- Prevalence: 62.7% (94 repos)
- Node Type: `assignment_expression`

**Examples:**

```javascript
url = await this.storageAdapter.getPreviewUrl(bucket, path, expiresIn, respHeaders)
```
*apps/nestjs-backend/src/features/attachments/attachments-storage.service.ts*

```javascript
finalData = await this.getCommentDetail(commentId)
```
*apps/nestjs-backend/src/features/comment/comment-open-api.service.ts*


### 88. IDENTIFIER.stringify(IDENTIFIER)

**Statistics:**
- Frequency: 6,610 occurrences
- Prevalence: 81.3% (122 repos)
- Node Type: `call_expression`
- Semantic: `JSON.stringify(IDENTIFIER)`

**Examples:**

```javascript
JSON.stringify(durationInput)
```
*packages/core/src/structs/view-spec.ts*

```javascript
JSON.stringify(command)
```
*scripts/src/utils/exec.ts*


### 90. IDENTIFIER.json

**Statistics:**
- Frequency: 6,603 occurrences
- Prevalence: 52.0% (78 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
response.json
```
*packages/web3-providers-http/src/index.ts*

```javascript
response.json
```
*packages/web3-providers-http/src/index.ts*


### 105. const IDENTIFIER = await EXPRESSION

**Statistics:**
- Frequency: 6,040 occurrences
- Prevalence: 42.7% (64 repos)
- Node Type: `lexical_declaration`
- Semantic: `const res = await EXPRESSION`

**Examples:**

```javascript
const res = await this.storageAdapter.presigned(bucket, dir, {
      ...presignedParams,
    });
```
*apps/nestjs-backend/src/features/attachments/attachments.service.ts*

```javascript
const res = await this.prismaService.$tx(async (prisma) => {
      if (user) {
        return await prisma.user.update({
          where: { id: user.id, deletedTime: null },
          data: {
        
```
*apps/nestjs-backend/src/features/auth/local-auth/local-auth.service.ts*


### 189. IDENTIFIER.json()

**Statistics:**
- Frequency: 3,518 occurrences
- Prevalence: 41.3% (62 repos)
- Node Type: `call_expression`

**Examples:**

```javascript
response.json()
```
*packages/web3-providers-http/src/index.ts*

```javascript
response.json()
```
*packages/web3-providers-http/src/index.ts*


---

## ERROR_HANDLING

*2 patterns, 21,068 total occurrences*

### 42. IDENTIFIER.error

**Statistics:**
- Frequency: 13,091 occurrences
- Prevalence: 69.3% (104 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
body.error
```
*packages/google-calendar/src/event-source-def.ts*

```javascript
body.error
```
*packages/google-calendar/src/event-source-def.ts*


### 69. IDENTIFIER.error

**Statistics:**
- Frequency: 7,977 occurrences
- Prevalence: 86.0% (129 repos)
- Node Type: `member_expression`
- Semantic: `console.error`

**Examples:**

```javascript
console.error
```
*scripts/src/pkg/bundle.ts*

```javascript
console.error
```
*scripts/src/pkg/utils/rollup-presets.ts*


---

## EXPRESSIONS

*12 patterns, 86,485 total occurrences*

### 30. IDENTIFIER.log

**Statistics:**
- Frequency: 21,113 occurrences
- Prevalence: 88.0% (132 repos)
- Node Type: `member_expression`
- Semantic: `console.log`

**Examples:**

```javascript
console.log
```
*scripts/src/archive.ts*

```javascript
console.log
```
*scripts/src/test.ts*


### 50. IDENTIFIER.fn

**Statistics:**
- Frequency: 10,805 occurrences
- Prevalence: 28.0% (42 repos)
- Node Type: `member_expression`
- Semantic: `vi.fn`

**Examples:**

```javascript
vi.fn
```
*apps/nestjs-backend/src/configs/config.spec.ts*

```javascript
vi.fn
```
*apps/nestjs-backend/src/features/aggregation/open-api/aggregation-open-api.controller.spec.ts*


### 72. IDENTIFIER.fn

**Statistics:**
- Frequency: 7,828 occurrences
- Prevalence: 27.3% (41 repos)
- Node Type: `member_expression`
- Semantic: `jest.fn`

**Examples:**

```javascript
jest.fn
```
*packages/web3/test/integration/contract-middleware.test.ts*

```javascript
jest.fn
```
*packages/web3/test/integration/contract-middleware.test.ts*


### 78. IDENTIFIER.isArray

**Statistics:**
- Frequency: 7,271 occurrences
- Prevalence: 80.0% (120 repos)
- Node Type: `member_expression`
- Semantic: `Array.isArray`

**Examples:**

```javascript
Array.isArray
```
*packages/core/src/datelib/env.ts*

```javascript
Array.isArray
```
*packages/core/src/datelib/locale.ts*


### 79. IDENTIFIER.now

**Statistics:**
- Frequency: 7,237 occurrences
- Prevalence: 72.7% (109 repos)
- Node Type: `member_expression`
- Semantic: `Date.now`

**Examples:**

```javascript
Date.now
```
*packages/core/src/reducers/CalendarNowManager.ts*

```javascript
Date.now
```
*packages/core/src/reducers/CalendarNowManager.ts*


### 91. new IDENTIFIER()

**Statistics:**
- Frequency: 6,465 occurrences
- Prevalence: 69.3% (104 repos)
- Node Type: `new_expression`
- Semantic: `new Date()`

**Examples:**

```javascript
new Date()
```
*packages/core/src/datelib/env.ts*

```javascript
new Date()
```
*packages/core/src/datelib/env.ts*


### 110. this.props

**Statistics:**
- Frequency: 5,805 occurrences
- Prevalence: 30.0% (45 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
this.props
```
*packages/core/src/CalendarContent.tsx*

```javascript
this.props
```
*packages/core/src/CalendarContent.tsx*


### 157. this.request

**Statistics:**
- Frequency: 4,235 occurrences
- Prevalence: 14.0% (21 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
this.request
```
*packages/web3-errors/src/errors/response_errors.ts*

```javascript
this.request
```
*packages/web3-errors/src/errors/response_errors.ts*


### 160. IDENTIFIER.from

**Statistics:**
- Frequency: 4,158 occurrences
- Prevalence: 73.3% (110 repos)
- Node Type: `member_expression`
- Semantic: `Array.from`

**Examples:**

```javascript
Array.from
```
*apps/nestjs-backend/src/event-emitter/event-emitter.service.ts*

```javascript
Array.from
```
*apps/nestjs-backend/src/event-emitter/listeners/record-history.listener.ts*


### 164. this.options

**Statistics:**
- Frequency: 4,013 occurrences
- Prevalence: 46.7% (70 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
this.options
```
*packages/core/src/common/Emitter.ts*

```javascript
this.options
```
*packages/core/src/common/Emitter.ts*


### 165. this.logger

**Statistics:**
- Frequency: 4,012 occurrences
- Prevalence: 24.7% (37 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
this.logger
```
*apps/nestjs-backend/src/event-emitter/event-emitter.service.ts*

```javascript
this.logger
```
*apps/nestjs-backend/src/event-emitter/event-emitter.service.ts*


### 188. IDENTIFIER.max

**Statistics:**
- Frequency: 3,543 occurrences
- Prevalence: 67.3% (101 repos)
- Node Type: `member_expression`
- Semantic: `Math.max`

**Examples:**

```javascript
Math.max
```
*packages/core/src/CalendarContent.tsx*

```javascript
Math.max
```
*packages/core/src/common/DaySeriesModel.ts*


---

## FUNCTION_CALLS

*3 patterns, 22,822 total occurrences*

### 57. IDENTIFIER.fn()

**Statistics:**
- Frequency: 9,364 occurrences
- Prevalence: 25.3% (38 repos)
- Node Type: `call_expression`
- Semantic: `vi.fn()`

**Examples:**

```javascript
vi.fn()
```
*apps/nestjs-backend/src/configs/config.spec.ts*

```javascript
vi.fn()
```
*apps/nestjs-backend/src/features/aggregation/open-api/aggregation-open-api.controller.spec.ts*


### 80. IDENTIFIER.now()

**Statistics:**
- Frequency: 7,192 occurrences
- Prevalence: 72.7% (109 repos)
- Node Type: `call_expression`
- Semantic: `Date.now()`

**Examples:**

```javascript
Date.now()
```
*packages/core/src/reducers/CalendarNowManager.ts*

```javascript
Date.now()
```
*packages/core/src/reducers/CalendarNowManager.ts*


### 97. IDENTIFIER.fn()

**Statistics:**
- Frequency: 6,266 occurrences
- Prevalence: 25.3% (38 repos)
- Node Type: `call_expression`
- Semantic: `jest.fn()`

**Examples:**

```javascript
jest.fn()
```
*packages/web3/test/integration/contract-middleware.test.ts*

```javascript
jest.fn()
```
*packages/web3/test/integration/contract.test.ts*


---

## FUNCTION_DEFINITIONS

*3 patterns, 412,050 total occurrences*

### 1. ( ) => BODY

**Statistics:**
- Frequency: 352,437 occurrences
- Prevalence: 100.0% (150 repos)
- Node Type: `arrow_function`

**Examples:**

```javascript
() => {
    if (this.isRendering) {
      this.isRendered = true
      let { currentData } = this

      flushSync(() => {
        render(
          <CalendarRoot options={currentData.calendarOptions}
```
*packages/core/src/Calendar.tsx*

```javascript
() => {
        render(
          <CalendarRoot options={currentData.calendarOptions} theme={currentData.theme} emitter={currentData.emitter}>
            {(classNames, height, isHeightAuto, forPrint)
```
*packages/core/src/Calendar.tsx*


### 9. () => BODY

**Statistics:**
- Frequency: 53,567 occurrences
- Prevalence: 53.3% (80 repos)
- Node Type: `arrow_function`

**Examples:**

```javascript
vevent => new ICAL.Event(vevent)
```
*packages/icalendar/src/ical-expander/IcalExpander.js*

```javascript
e => !e.isRecurrenceException()
```
*packages/icalendar/src/ical-expander/IcalExpander.js*


### 104. IDENTIFIER(( ) => BODY)

**Statistics:**
- Frequency: 6,046 occurrences
- Prevalence: 50.7% (76 repos)
- Node Type: `call_expression`
- Semantic: `expect(( ) => BODY)`

**Examples:**

```javascript
expect(() => storage.verifyReadToken('expired-token'))
```
*apps/nestjs-backend/src/features/attachments/plugins/local.spec.ts*

```javascript
expect(() => storage.verifyReadToken('invalid-token'))
```
*apps/nestjs-backend/src/features/attachments/plugins/local.spec.ts*


---

## OBJECT_OPERATIONS

*4 patterns, 21,870 total occurrences*

### 65. IDENTIFIER.keys

**Statistics:**
- Frequency: 8,809 occurrences
- Prevalence: 84.0% (126 repos)
- Node Type: `member_expression`
- Semantic: `Object.OBJECT_KEYS`

**Examples:**

```javascript
Object.keys
```
*packages/core/src/api/CalendarImpl.ts*

```javascript
Object.keys
```
*packages/core/src/api/EventImpl.ts*


### 106. IDENTIFIER.keys(IDENTIFIER)

**Statistics:**
- Frequency: 5,990 occurrences
- Prevalence: 80.0% (120 repos)
- Node Type: `call_expression`
- Semantic: `Object.OBJECT_KEYS(IDENTIFIER)`

**Examples:**

```javascript
Object.keys(standardDateProps)
```
*packages/core/src/datelib/formatting-native.ts*

```javascript
Object.keys(hash)
```
*packages/core/src/util/object.ts*


### 185. IDENTIFIER.entries

**Statistics:**
- Frequency: 3,640 occurrences
- Prevalence: 70.0% (105 repos)
- Node Type: `member_expression`
- Semantic: `Object.OBJECT_ENTRIES`

**Examples:**

```javascript
Object.entries
```
*apps/nestjs-backend/src/event-emitter/event-emitter.service.ts*

```javascript
Object.entries
```
*apps/nestjs-backend/src/event-emitter/listeners/action-trigger.listener.ts*


### 197. IDENTIFIER.defineProperty

**Statistics:**
- Frequency: 3,431 occurrences
- Prevalence: 48.0% (72 repos)
- Node Type: `member_expression`
- Semantic: `Object.defineProperty`

**Examples:**

```javascript
Object.defineProperty
```
*packages/web3-eth-accounts/test/unit/tx/eip1559.test.ts*

```javascript
Object.defineProperty
```
*packages/web3-eth-accounts/test/unit/tx/legacy.test.ts*


---

## REACT_PATTERNS

*2 patterns, 13,688 total occurrences*

### 67. import * as IDENTIFIER from ' react ' ;

**Statistics:**
- Frequency: 8,684 occurrences
- Prevalence: 20.7% (31 repos)
- Node Type: `import_statement`
- Semantic: `import * as React from ' react ' ;`

**Examples:**

```javascript
import * as React from 'react';
```
*apps/nextjs-app/src/features/app/blocks/design/data-table/DataTable.tsx*

```javascript
import * as React from 'react';
```
*packages/icons/src/components/A.tsx*


### 131. import IDENTIFIER from ' react ' ;

**Statistics:**
- Frequency: 5,004 occurrences
- Prevalence: 29.3% (44 repos)
- Node Type: `import_statement`
- Semantic: `import React from ' react ' ;`

**Examples:**

```javascript
import React from 'react';
```
*apps/nextjs-app/config/tests/ReactSvgrMock.tsx*

```javascript
import React from 'react';
```
*apps/nextjs-app/src/features/app/blocks/chart/components/EnvProvider.tsx*


---

## STATE_MANAGEMENT

*3 patterns, 15,417 total occurrences*

### 115. this.state

**Statistics:**
- Frequency: 5,664 occurrences
- Prevalence: 37.3% (56 repos)
- Node Type: `member_expression`

**Examples:**

```javascript
this.state
```
*packages/core/src/CalendarContent.tsx*

```javascript
this.state
```
*packages/core/src/CalendarRoot.tsx*


### 132. IDENTIFIER(BOOLEAN)

**Statistics:**
- Frequency: 4,982 occurrences
- Prevalence: 46.7% (70 repos)
- Node Type: `call_expression`
- Semantic: `useState(BOOLEAN)`

**Examples:**

```javascript
useState(false)
```
*apps/nextjs-app/src/components/Guide.tsx*

```javascript
useState(false)
```
*apps/nextjs-app/src/features/app/automation/workflow-panel/WorkFlowPanelModal.tsx*


### 136. const [ IDENTIFIER , IDENTIFIER ] = IDENTIFIER(BOOLEAN)

**Statistics:**
- Frequency: 4,771 occurrences
- Prevalence: 46.7% (70 repos)
- Node Type: `lexical_declaration`
- Semantic: `const [ IDENTIFIER , IDENTIFIER ] = useState(BOOLEAN)`

**Examples:**

```javascript
const [run, setRun] = useState(false);
```
*apps/nextjs-app/src/components/Guide.tsx*

```javascript
const [open, setOpen] = useState(false);
```
*apps/nextjs-app/src/features/app/automation/workflow-panel/WorkFlowPanelModal.tsx*


---

## TEST_PATTERNS

*7 patterns, 58,126 total occurrences*

### 16. IDENTIFIER(IDENTIFIER).toBe

**Statistics:**
- Frequency: 28,617 occurrences
- Prevalence: 64.7% (97 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER).ASSERTION`

**Examples:**

```javascript
expect(selectFired).toBe
```
*tests/src/date-selection/implicit-unselect.ts*

```javascript
expect(unselectFired).toBe
```
*tests/src/date-selection/implicit-unselect.ts*


### 84. IDENTIFIER(IDENTIFIER).toBe(NUMBER)

**Statistics:**
- Frequency: 6,896 occurrences
- Prevalence: 46.7% (70 repos)
- Node Type: `call_expression`
- Semantic: `expect(IDENTIFIER).ASSERTION(NUMBER)`

**Examples:**

```javascript
expect(selectFired).toBe(1)
```
*tests/src/date-selection/implicit-unselect.ts*

```javascript
expect(unselectFired).toBe(0)
```
*tests/src/date-selection/implicit-unselect.ts*


### 112. IDENTIFIER(IDENTIFIER).toHaveBeenCalled

**Statistics:**
- Frequency: 5,730 occurrences
- Prevalence: 42.7% (64 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER).SPY_ASSERTION`

**Examples:**

```javascript
expect(viewDidMountSpy).toHaveBeenCalled
```
*tests/src/legacy/View.ts*

```javascript
expect(navLinkDayClickSpy).toHaveBeenCalled
```
*tests/src/legacy/navLinks.ts*


### 126. IDENTIFIER(await EXPRESSION)

**Statistics:**
- Frequency: 5,097 occurrences
- Prevalence: 38.7% (58 repos)
- Node Type: `call_expression`
- Semantic: `expect(await EXPRESSION)`

**Examples:**

```javascript
expect(await contract.methods.name().call())
```
*packages/web3/test/cjs_black_box/test/web3-eth-contract/erc20.test.ts*

```javascript
expect(await contract.methods.symbol().call())
```
*packages/web3/test/cjs_black_box/test/web3-eth-contract/erc20.test.ts*


### 146. IDENTIFIER.any

**Statistics:**
- Frequency: 4,388 occurrences
- Prevalence: 33.3% (50 repos)
- Node Type: `member_expression`
- Semantic: `expect.any`

**Examples:**

```javascript
expect.any
```
*apps/nestjs-backend/src/features/access-token/access-token.service.spec.ts*

```javascript
expect.any
```
*apps/nestjs-backend/src/features/auth/session/session-store.service.spec.ts*


### 173. IDENTIFIER(IDENTIFIER).toBe(IDENTIFIER)

**Statistics:**
- Frequency: 3,893 occurrences
- Prevalence: 55.3% (83 repos)
- Node Type: `call_expression`
- Semantic: `expect(IDENTIFIER).ASSERTION(IDENTIFIER)`

**Examples:**

```javascript
expect(newEvent).toBe(event)
```
*tests/src/event-data/Calendar.addEvent.ts*

```javascript
expect(newEvent).toBe(event)
```
*tests/src/event-data/Calendar.addEvent.ts*


### 190. IDENTIFIER(IDENTIFIER.length).toBe

**Statistics:**
- Frequency: 3,505 occurrences
- Prevalence: 38.7% (58 repos)
- Node Type: `member_expression`
- Semantic: `expect(IDENTIFIER.length).ASSERTION`

**Examples:**

```javascript
expect(events.length).toBe
```
*tests/src/datelib/rrule.ts*

```javascript
expect(events.length).toBe
```
*tests/src/datelib/rrule.ts*


---

