import { computed, reactive, watch } from 'vue'

const STORAGE_KEY = 'adx-traffic-group-vue'

export const metricColumns = [
  { key: 'price', label: '价格', type: 'currency', info: true },
  { key: 'estimatedRevenue', label: '预估收入', type: 'number', info: true },
  { key: 'profitPerMille', label: '千人均收益', type: 'currency', info: true },
  { key: 'ecpm', label: 'eCPM', type: 'currency', info: true },
  { key: 'requestValue', label: '千次请求价值', type: 'currency', info: true },
  { key: 'requestVolume', label: '请求量', type: 'volume', info: false },
  { key: 'returnRate', label: '返回率', type: 'percent', info: true },
  { key: 'bidSuccessCount', label: '竞价成功数', type: 'volume', info: false },
  { key: 'bidSuccessRate', label: '竞价成功率', type: 'percent', info: true },
  { key: 'impressionCount', label: '展示量', type: 'volume', info: true },
  { key: 'winRate', label: '竞胜展示率', type: 'percent', info: true },
  { key: 'clickRate', label: '点击率', type: 'percent', info: true },
  { key: 'cpc', label: 'cpc', type: 'currency', info: true }
]

export function useTrafficGroupManager() {
  const state = reactive(loadState())

  const currentKey = computed(() => `${state.filters.scene}|${state.filters.platform}`)
  const currentDataset = computed(() => state.datasets[currentKey.value])
  const currentGroups = computed(() => currentDataset.value.groups)
  const currentSlots = computed(() => currentDataset.value.slots)
  const currentGroup = computed(() => ensureCurrentGroup())
  const sortedPids = computed(() => sortPids(currentGroup.value.pids, state.sort))
  const summary = computed(() => computeSummary(currentGroup.value.pids))
  const dspCatalog = computed(() => buildDspCatalog(state.datasets))

  watch(
    () => currentKey.value,
    () => {
      ensureCurrentGroup()
    },
    { immediate: true }
  )

  watch(
    state,
    value => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(value))
    },
    { deep: true }
  )

  function ensureCurrentGroup() {
    const groups = currentDataset.value.groups
    let group = groups.find(item => item.id === state.currentGroupId)
    if (!group) {
      group = groups[0]
      state.currentGroupId = group.id
    }
    return group
  }

  function switchGroup(groupId) {
    state.currentGroupId = groupId
  }

  function setSort(key) {
    if (state.sort.key === key) {
      state.sort.direction = state.sort.direction === 'asc' ? 'desc' : 'asc'
      return
    }
    state.sort.key = key
    state.sort.direction = 'desc'
  }

  function toggleGroupEnabled() {
    currentGroup.value.enabled = !currentGroup.value.enabled
    return currentGroup.value.enabled
  }

  function togglePidEnabled(pidId) {
    const pid = findPid(pidId)
    pid.enabled = !pid.enabled
    return pid
  }

  function updatePrice(pidId, price) {
    const pid = findPid(pidId)
    pid.price = Number(price) || 0
    return pid
  }

  function upsertGroup(payload, groupId = '') {
    const groups = currentDataset.value.groups
    const existing = groupId ? groups.find(item => item.id === groupId) : null
    const group = existing || {
      id: uid(),
      enabled: true,
      isAbTest: false,
      pids: []
    }

    group.name = payload.name.trim()
    group.priority = Number(payload.priority) || 1
    group.scene = state.filters.scene
    group.platform = state.filters.platform
    group.slot = payload.slot
    group.note = payload.note.trim()
    group.rules = payload.rules.map(rule => ({
      field: rule.field.trim() || '用户标签',
      operator: rule.operator.trim() || '等于',
      value: rule.value.trim() || '全部用户'
    }))

    if (!existing) {
      groups.push(group)
    }

    groups.sort((left, right) => left.priority - right.priority)
    state.currentGroupId = group.id
    return group
  }

  function duplicateGroup(groupId) {
    const source = currentGroups.value.find(item => item.id === groupId)
    const clone = deepCopy(source)
    clone.id = uid()
    clone.name = `${source.name}-复制`
    clone.priority = Math.max(...currentGroups.value.map(item => item.priority)) + 1
    clone.isAbTest = false
    clone.pids = clone.pids.map(pid => ({ ...pid, id: uid() }))
    currentGroups.value.push(clone)
    currentGroups.value.sort((left, right) => left.priority - right.priority)
    state.currentGroupId = clone.id
    return clone
  }

  function removeGroup(groupId) {
    const groups = currentGroups.value
    if (groups.length === 1) {
      return null
    }
    const index = groups.findIndex(item => item.id === groupId)
    if (index === -1) {
      return null
    }
    const [removed] = groups.splice(index, 1)
    state.currentGroupId = groups[0].id
    return removed
  }

  function createAbGroup(payload) {
    const source = deepCopy(currentGroup.value)
    const traffic = Number(payload.traffic) || 30
    source.id = uid()
    source.name = payload.name.trim()
    source.priority = Number(payload.priority) || currentGroup.value.priority + 1
    source.note = `A/B流量 ${traffic}% · ${payload.note.trim()}`
    source.isAbTest = true
    source.pids = source.pids.map(pid => ({
      ...pid,
      id: uid(),
      price: round(pid.price * (1 + traffic / 500), 2)
    }))
    currentGroups.value.push(source)
    currentGroups.value.sort((left, right) => left.priority - right.priority)
    state.currentGroupId = source.id
    return source
  }

  function upsertPid(payload, pidId = '') {
    const group = currentGroup.value
    const existing = pidId ? group.pids.find(item => item.id === pidId) : null
    const template = payload.templateName ? findDspTemplate(dspCatalog.value, payload.templateName) : null
    const pid = existing || createPid({
      name: payload.name,
      pidCode: payload.pidCode || '',
      price: Number(payload.price ?? template?.price) || 0,
      statusColor: payload.statusColor || template?.statusColor || 'green',
      estimatedRevenue: template?.estimatedRevenue,
      profitPerMille: template?.profitPerMille,
      ecpm: template?.ecpm,
      requestValue: template?.requestValue,
      requestVolume: template?.requestVolume,
      returnRate: template?.returnRate,
      bidSuccessCount: template?.bidSuccessCount,
      bidSuccessRate: template?.bidSuccessRate,
      impressionCount: template?.impressionCount,
      winRate: template?.winRate,
      clickRate: template?.clickRate,
      cpc: template?.cpc
    })

    Object.assign(pid, {
      name: payload.name.trim(),
      pidCode: String(payload.pidCode || '').trim(),
      price: Number(payload.price ?? template?.price ?? pid.price) || 0,
      statusColor: payload.statusColor || template?.statusColor || pid.statusColor,
      enabled: payload.enabled,
      estimatedRevenue: Number(payload.estimatedRevenue ?? template?.estimatedRevenue ?? pid.estimatedRevenue) || 0,
      profitPerMille: Number(payload.profitPerMille ?? template?.profitPerMille ?? pid.profitPerMille) || 0,
      ecpm: Number(payload.ecpm ?? template?.ecpm ?? pid.ecpm) || 0,
      requestValue: Number(payload.requestValue ?? template?.requestValue ?? pid.requestValue) || 0,
      requestVolume: Number(payload.requestVolume ?? template?.requestVolume ?? pid.requestVolume) || 0,
      returnRate: Number(payload.returnRate ?? template?.returnRate ?? pid.returnRate) || 0,
      bidSuccessCount: Number(payload.bidSuccessCount ?? template?.bidSuccessCount ?? pid.bidSuccessCount) || 0,
      bidSuccessRate: Number(payload.bidSuccessRate ?? template?.bidSuccessRate ?? pid.bidSuccessRate) || 0,
      impressionCount: Number(payload.impressionCount ?? template?.impressionCount ?? pid.impressionCount) || 0,
      winRate: Number(payload.winRate ?? template?.winRate ?? pid.winRate) || 0,
      clickRate: Number(payload.clickRate ?? template?.clickRate ?? pid.clickRate) || 0,
      cpc: Number(payload.cpc ?? template?.cpc ?? pid.cpc) || 0
    })

    if (!existing) {
      group.pids.push(pid)
    }

    return pid
  }

  function removePid(pidId) {
    const group = currentGroup.value
    const index = group.pids.findIndex(item => item.id === pidId)
    if (index === -1) {
      return null
    }
    const [removed] = group.pids.splice(index, 1)
    return removed
  }

  function findPid(pidId) {
    return currentGroup.value.pids.find(item => item.id === pidId)
  }

  return {
    state,
    metricColumns,
    currentGroups,
    currentSlots,
    currentGroup,
    sortedPids,
    summary,
    dspCatalog,
    switchGroup,
    setSort,
    toggleGroupEnabled,
    togglePidEnabled,
    updatePrice,
    upsertGroup,
    duplicateGroup,
    removeGroup,
    createAbGroup,
    upsertPid,
    removePid,
    findPid
  }
}

function loadState() {
  const fallbackDatasets = buildBaseMatrix()
  const fallback = {
    filters: { scene: '开屏', platform: 'iOS' },
    currentGroupId: fallbackDatasets['开屏|iOS'].groups[0].id,
    sort: { key: 'estimatedRevenue', direction: 'desc' },
    datasets: fallbackDatasets
  }

  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) {
      return fallback
    }
    const parsed = JSON.parse(stored)
    if (!parsed?.datasets) {
      return fallback
    }
    return parsed
  } catch {
    return fallback
  }
}

function buildBaseMatrix() {
  return {
    '开屏|iOS': {
      slots: ['1000 - 美柚--开屏', '1001 - 美柚--开屏兜底', '1002 - 美柚--开屏实验位'],
      groups: [
        {
          id: uid(),
          name: '默认分组',
          priority: 1,
          scene: '开屏',
          platform: 'iOS',
          slot: '1000 - 美柚--开屏',
          enabled: true,
          isAbTest: false,
          note: '基础放量组',
          rules: [
            { field: '用户活跃度', operator: '高于', value: '近7日活跃 >= 3' },
            { field: '系统版本', operator: '包含', value: 'iOS 17' }
          ],
          pids: [
            createPid({ name: '穿山甲-开屏iOS', price: 18.5, statusColor: 'green', requestVolume: 168000, returnRate: 56.7, bidSuccessCount: 42000, bidSuccessRate: 44.2, impressionCount: 65000, winRate: 100, clickRate: 5, cpc: 1.85 }),
            createPid({ name: '快手-开屏iOS', price: 15.2, statusColor: 'orange', requestVolume: 88000, returnRate: 57.2, bidSuccessCount: 18000, bidSuccessRate: 36.2, impressionCount: 38000, winRate: 100, clickRate: 4, cpc: 1.02 })
          ]
        }
      ]
    },
    '开屏|Android': {
      slots: ['2000 - 美柚--开屏Android', '2001 - 美柚--开屏Android兜底'],
      groups: [
        {
          id: uid(),
          name: '默认分组',
          priority: 1,
          scene: '开屏',
          platform: 'Android',
          slot: '2000 - 美柚--开屏Android',
          enabled: true,
          isAbTest: false,
          note: 'Android基线组',
          rules: [{ field: '机型等级', operator: '属于', value: '中高端' }],
          pids: [
            createPid({ name: '广点通-开屏Android', price: 12.6, statusColor: 'green', requestVolume: 152000, returnRate: 59.8, bidSuccessCount: 53000, bidSuccessRate: 40.3, impressionCount: 72000, winRate: 82, clickRate: 3.7, cpc: 0.92 }),
            createPid({ name: '百度-开屏Android', price: 10.8, statusColor: 'gray', requestVolume: 92000, returnRate: 49.2, bidSuccessCount: 21000, bidSuccessRate: 28.4, impressionCount: 35000, winRate: 73, clickRate: 2.9, cpc: 0.88, enabled: false })
          ]
        }
      ]
    },
    '信息流|iOS': {
      slots: ['3000 - 美柚--信息流首刷', '3001 - 美柚--信息流下滑'],
      groups: [
        {
          id: uid(),
          name: '默认分组',
          priority: 1,
          scene: '信息流',
          platform: 'iOS',
          slot: '3000 - 美柚--信息流首刷',
          enabled: true,
          isAbTest: false,
          note: '信息流首刷测试中',
          rules: [{ field: '访问深度', operator: '高于', value: '3页' }],
          pids: [
            createPid({ name: '穿山甲-信息流iOS', price: 9.8, statusColor: 'green', requestVolume: 245000, returnRate: 66.5, bidSuccessCount: 102000, bidSuccessRate: 51.5, impressionCount: 86000, winRate: 74, clickRate: 2.6, cpc: 0.76 }),
            createPid({ name: '快手-信息流iOS', price: 8.4, statusColor: 'orange', requestVolume: 198000, returnRate: 58.1, bidSuccessCount: 74000, bidSuccessRate: 46.8, impressionCount: 63000, winRate: 69, clickRate: 2.2, cpc: 0.64 })
          ]
        }
      ]
    },
    '信息流|Android': {
      slots: ['4000 - 美柚--信息流Android', '4001 - 美柚--信息流Android补量'],
      groups: [
        {
          id: uid(),
          name: '默认分组',
          priority: 1,
          scene: '信息流',
          platform: 'Android',
          slot: '4000 - 美柚--信息流Android',
          enabled: true,
          isAbTest: false,
          note: 'Android信息流补量',
          rules: [
            { field: '新用户', operator: '等于', value: '是' },
            { field: '频道', operator: '属于', value: '备孕/母婴' }
          ],
          pids: [
            createPid({ name: '优量汇-信息流Android', price: 7.3, statusColor: 'green', requestVolume: 176000, returnRate: 61.2, bidSuccessCount: 58000, bidSuccessRate: 43.7, impressionCount: 54000, winRate: 68, clickRate: 1.9, cpc: 0.51 }),
            createPid({ name: '百度-信息流Android', price: 6.2, statusColor: 'orange', requestVolume: 129000, returnRate: 54.6, bidSuccessCount: 34000, bidSuccessRate: 38.2, impressionCount: 42000, winRate: 63, clickRate: 1.6, cpc: 0.48 })
          ]
        }
      ]
    }
  }
}

function createPid({ name, pidCode = '', price, statusColor = 'green', estimatedRevenue, profitPerMille, ecpm, requestValue, requestVolume = 64000, returnRate = 52.4, bidSuccessCount = 16000, bidSuccessRate = 38.5, impressionCount = 31000, winRate = 74.2, clickRate = 2.8, cpc = 0.86, enabled = true }) {
  return {
    id: uid(),
    name,
    pidCode,
    enabled,
    statusColor,
    price,
    estimatedRevenue: estimatedRevenue ?? round(requestVolume * price / 206, 1),
    profitPerMille: profitPerMille ?? round(price / 205, 2),
    ecpm: ecpm ?? round(price * 1.2, 2),
    requestValue: requestValue ?? round(price / 18, 2),
    requestVolume,
    returnRate,
    bidSuccessCount,
    bidSuccessRate,
    impressionCount,
    winRate,
    clickRate,
    cpc
  }
}

function computeSummary(pids) {
  const enabled = pids.filter(pid => pid.enabled)
  const source = enabled.length ? enabled : pids
  const result = {}
  metricColumns.forEach(column => {
    if (['requestVolume', 'bidSuccessCount', 'impressionCount'].includes(column.key)) {
      result[column.key] = source.reduce((sum, pid) => sum + pid[column.key], 0)
      return
    }
    result[column.key] = round(source.reduce((sum, pid) => sum + pid[column.key], 0) / Math.max(source.length, 1), 2)
  })
  return result
}

function sortPids(pids, sort) {
  const factor = sort.direction === 'asc' ? 1 : -1
  return [...pids].sort((left, right) => {
    if (left[sort.key] === right[sort.key]) {
      return left.name.localeCompare(right.name, 'zh-CN') * factor
    }
    return (left[sort.key] - right[sort.key]) * factor
  })
}

function uid() {
  return Math.random().toString(36).slice(2, 10)
}

function deepCopy(value) {
  return JSON.parse(JSON.stringify(value))
}

function round(value, digits = 2) {
  const factor = 10 ** digits
  return Math.round(Number(value) * factor) / factor
}

function buildDspCatalog(datasets) {
  const map = new Map()
  Object.values(datasets).forEach(dataset => {
    dataset.groups.forEach(group => {
      group.pids.forEach(pid => {
        if (!map.has(pid.name)) {
          map.set(pid.name, deepCopy(pid))
        }
      })
    })
  })
  return Array.from(map.values())
}

function findDspTemplate(dspCatalog, name) {
  return dspCatalog.find(item => item.name === name) || null
}