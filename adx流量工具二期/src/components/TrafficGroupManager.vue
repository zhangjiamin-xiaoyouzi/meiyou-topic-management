<template>
  <div class="traffic-app">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-badge">⌂</span>
        <span>广告投放运营后台</span>
      </div>

      <div class="nav-list">
        <button v-for="item in primaryMenus" :key="item" class="nav-item" type="button">
          <span class="nav-main"><span class="nav-icon"></span><span class="nav-label">{{ item }}</span></span>
        </button>

        <div class="nav-group open">
          <button class="nav-item active" type="button">
            <span class="nav-main"><span class="nav-icon"></span><span class="nav-label">ADX流量工具</span></span>
            <span class="nav-arrow">⌃</span>
          </button>
          <div class="nav-sublist">
            <button
              v-for="item in pageMenus"
              :key="item.key"
              :class="['nav-subitem', { active: currentPage === item.key }]"
              type="button"
              @click="currentPage = item.key"
            >
              <span class="nav-main"><span class="nav-label">{{ item.label }}</span></span>
            </button>
          </div>
        </div>
      </div>
    </aside>

    <main class="content">
      <header class="topbar">
        <div class="breadcrumbs">
          <span>ADX流量工具</span>
          <span class="crumb-sep"></span>
          <strong>{{ currentPageLabel }}</strong>
        </div>
      </header>

      <section v-if="currentPage === 'group'" class="page">
        <div class="filter-bar card card-soft">
          <label class="filter-item">
            <span>广告场景：</span>
            <div class="select-wrap">
              <select v-model="state.filters.scene">
                <option v-for="scene in scenes" :key="scene" :value="scene">{{ scene }}</option>
              </select>
            </div>
          </label>

          <label class="filter-item">
            <span>平台：</span>
            <div class="select-wrap select-chip">
              <span class="chip-dot"></span>
              <select v-model="state.filters.platform" class="chip-select">
                <option v-for="platform in platforms" :key="platform" :value="platform">{{ platform }}</option>
              </select>
            </div>
          </label>
        </div>

        <section class="card">
          <div class="card-header tight">
            <button class="outline-button" type="button" @click="openGroupModal()"><span class="plus">＋</span>添加分组</button>
          </div>

          <div class="group-tabs">
            <button
              v-for="group in currentGroups"
              :key="group.id"
              :class="['group-tab', { active: group.id === currentGroup.id }]"
              type="button"
              @click="switchGroup(group.id)"
            >
              <span>{{ group.name }}</span>
              <span v-if="group.isAbTest" class="ab-badge badge-inline">A/B</span>
              <span class="tiny-button" @click.stop="openGroupMenu(group.id, $event)">···</span>
            </button>
          </div>

          <div class="group-body">
            <div class="group-row">
              <div class="field-inline">
                <span>广告位：</span>
                <span class="tag">{{ currentGroup.slot }}</span>
              </div>
              <button class="outline-button" type="button" @click="openAbModal">创建A/B测试</button>
            </div>

            <div class="group-row">
              <div class="field-inline">
                <span>分组开关</span>
                <button :class="['switch', { on: currentGroup.enabled }]" type="button" @click="toggleGroupEnabledWithToast"></button>
              </div>
              <div class="footer-note">{{ groupMeta }}</div>
            </div>

            <div v-if="currentGroup.rules.length" class="rules-list">
              <div v-for="(rule, index) in currentGroup.rules" :key="`${rule.field}-${index}`" class="rule-item">
                <span>{{ rule.field }}</span>
                <span>{{ rule.operator }}</span>
                <span>{{ rule.value }}</span>
              </div>
            </div>
            <div v-else class="empty-state">当前分组未设置规则，默认全量命中</div>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <button class="outline-button" type="button" @click="openPidModal()"><span class="plus">＋</span>添加PID</button>
            <div class="footer-note">当前分组的汇总指标会随状态、价格和排序即时变化</div>
          </div>

          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>操作</th>
                  <th>DSP来源</th>
                  <th>状态</th>
                  <th v-for="column in metricColumns" :key="column.key">
                    <button :class="['sortable', { active: state.sort.key === column.key }]" type="button" @click="setSort(column.key)">
                      <span>{{ column.label }}</span>
                      <span v-if="column.info" class="metric-tip">i</span>
                      <span :class="['sort-arrow', { active: state.sort.key === column.key }]">{{ sortIndicator(column.key) }}</span>
                    </button>
                  </th>
                </tr>
              </thead>

              <tbody v-if="sortedPids.length">
                <tr class="summary-row">
                  <td></td>
                  <td>{{ enabledCount }}个DSP来源已启用</td>
                  <td></td>
                  <td v-for="column in metricColumns" :key="`summary-${column.key}`">{{ formatMetric(summary[column.key], column.type) }}</td>
                </tr>

                <tr v-for="pid in sortedPids" :key="pid.id">
                  <td><button class="edit-link" type="button" @click="openPidModal(pid.id)">编辑</button></td>
                  <td><span :class="['status-dot', pid.statusColor]" />{{ pid.name }}</td>
                  <td><button :class="['switch', { on: pid.enabled }]" type="button" @click="togglePidEnabledWithToast(pid.id)"></button></td>
                  <td v-for="column in metricColumns" :key="`${pid.id}-${column.key}`">
                    <span v-if="column.key === 'price'" class="editable-cell">
                      {{ formatMetric(pid[column.key], column.type) }}
                      <button class="icon-button" type="button" @click="openPriceModal(pid.id)"><span class="edit-icon">✎</span></button>
                    </span>
                    <template v-else>{{ formatMetric(pid[column.key], column.type) }}</template>
                  </td>
                </tr>
              </tbody>

              <tbody v-else>
                <tr>
                  <td colspan="16"><div class="empty-state">当前分组还没有PID，点击“添加PID”开始创建</div></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </section>

      <section v-else-if="currentPage === 'pid'" class="page">
        <div class="card card-soft filter-block">
          <div class="filter-grid pid-filter-grid">
            <label class="filter-item filter-item-stack">
              <span>广告场景</span>
              <div class="select-wrap"><select v-model="pidFilters.scene"><option value="全部场景">全部场景</option><option v-for="scene in scenes" :key="scene" :value="scene">{{ scene }}</option></select></div>
            </label>
            <label class="filter-item filter-item-stack">
              <span>平台</span>
              <div class="select-wrap"><select v-model="pidFilters.platform"><option value="全部平台">全部平台</option><option v-for="platform in platforms" :key="platform" :value="platform">{{ platform }}</option></select></div>
            </label>
            <label class="filter-item filter-item-stack">
              <span>广告位</span>
              <div class="select-wrap"><select v-model="pidFilters.slot"><option value="全部广告位">全部广告位</option><option v-for="slot in pidSlotOptions" :key="slot" :value="slot">{{ slot }}</option></select></div>
            </label>
            <div class="filter-action"><button class="brand-button" type="button">查询</button></div>
          </div>
        </div>

        <section class="card">
          <div class="card-header">
            <button class="outline-button" type="button" @click="openPidModal()"><span class="plus">＋</span>新增PID</button>
            <div class="footer-note">共{{ filteredPidRows.length }}条</div>
          </div>
          <div class="table-wrap">
            <table class="table-compact">
              <thead>
                <tr>
                  <th>PID</th>
                  <th>DSP来源</th>
                  <th>状态</th>
                  <th>平台</th>
                  <th>广告场景</th>
                  <th>广告位</th>
                  <th>绑定分组信息</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in pagedPidRows" :key="row.rowKey">
                  <td>{{ row.pid }}</td>
                  <td>{{ row.name }}</td>
                  <td><span :class="['status-pill', row.enabled ? 'status-pill-on' : 'status-pill-off']">{{ row.enabled ? '开启' : '停用' }}</span></td>
                  <td>{{ row.platform }}</td>
                  <td>{{ row.scene }}</td>
                  <td>{{ row.slot }}</td>
                  <td>{{ row.groupName }}</td>
                  <td class="table-actions">
                    <button class="edit-link" type="button" @click="openPidFromList(row)">编辑</button>
                    <button class="edit-link" type="button" @click="togglePidFromList(row)">{{ row.enabled ? '停用' : '启用' }}</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="pager">
            <button class="ghost-button" type="button" :disabled="pidPage === 1" @click="pidPage -= 1">上一页</button>
            <span>{{ pidPage }} / {{ pidPageCount }}</span>
            <button class="ghost-button" type="button" :disabled="pidPage === pidPageCount" @click="pidPage += 1">下一页</button>
          </div>
        </section>
      </section>

      <section v-else-if="currentPage === 'report'" class="page">
        <div class="card card-soft filter-block">
          <div class="filter-grid report-filter-grid">
            <label class="filter-item filter-item-stack filter-wide">
              <span>日期</span>
              <div class="date-range">
                <input v-model="reportFilters.start" type="date" />
                <span>→</span>
                <input v-model="reportFilters.end" type="date" />
              </div>
            </label>
            <label class="filter-item filter-item-stack">
              <span>广告场景</span>
              <div class="select-wrap"><select v-model="reportFilters.scene"><option value="全部">全部</option><option v-for="scene in scenes" :key="scene" :value="scene">{{ scene }}</option></select></div>
            </label>
            <label class="filter-item filter-item-stack">
              <span>平台</span>
              <div class="select-wrap"><select v-model="reportFilters.platform"><option value="全部">全部</option><option v-for="platform in platforms" :key="platform" :value="platform">{{ platform }}</option></select></div>
            </label>
            <label class="filter-item filter-item-stack">
              <span>分组</span>
              <div class="select-wrap"><select v-model="reportFilters.group"><option value="全部分组">全部分组</option><option v-for="item in reportGroupOptions" :key="item" :value="item">{{ item }}</option></select></div>
            </label>
            <div class="filter-action"><button class="brand-button" type="button">查询</button></div>
          </div>
        </div>

        <section class="card">
          <div class="card-header">
            <div class="section-title">数据图表</div>
            <div class="section-inline">
              <div class="select-wrap select-inline"><select v-model="reportMetric"><option v-for="item in reportMetricOptions" :key="item.key" :value="item.key">{{ item.label }}</option></select></div>
            </div>
          </div>
          <div class="chart-panel">
            <svg class="line-chart" viewBox="0 0 780 260" preserveAspectRatio="none">
              <line v-for="tick in 5" :key="tick" :x1="40" :x2="750" :y1="25 + (tick - 1) * 50" :y2="25 + (tick - 1) * 50" class="chart-grid" />
              <polyline :points="reportChartPoints" class="chart-line" />
              <circle v-for="point in reportChartCircles" :key="point.x" :cx="point.x" :cy="point.y" r="4" class="chart-dot" />
            </svg>
            <div class="chart-axis">
              <span v-for="row in reportRows" :key="row.date">{{ row.date }}</span>
            </div>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <div class="section-title">数据指标</div>
            <button class="outline-button" type="button" @click="exportTable(reportRows, '综合报表')">导出</button>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>日期</th>
                  <th>千人均收益</th>
                  <th>预估收入</th>
                  <th>eCPM</th>
                  <th>千次请求价值</th>
                  <th>请求量</th>
                  <th>返回率</th>
                  <th>竞价成功数</th>
                  <th>竞价成功率</th>
                  <th>展示量</th>
                  <th>竞胜展示率</th>
                  <th>点击数</th>
                  <th>点击率</th>
                  <th>cpc</th>
                </tr>
              </thead>
              <tbody>
                <tr class="summary-row">
                  <td>总计</td>
                  <td>{{ reportSummary.rpm }}</td>
                  <td>{{ reportSummary.income }}</td>
                  <td>{{ reportSummary.ecpm }}</td>
                  <td>{{ reportSummary.reqValue }}</td>
                  <td>{{ reportSummary.requests }}</td>
                  <td>{{ reportSummary.responseRate }}</td>
                  <td>{{ reportSummary.wins }}</td>
                  <td>{{ reportSummary.winRate }}</td>
                  <td>{{ reportSummary.impressions }}</td>
                  <td>{{ reportSummary.showRate }}</td>
                  <td>{{ reportSummary.clicks }}</td>
                  <td>{{ reportSummary.ctr }}</td>
                  <td>{{ reportSummary.cpc }}</td>
                </tr>
                <tr v-for="row in reportRows" :key="row.date">
                  <td>{{ row.date }}</td>
                  <td>{{ row.rpm }}</td>
                  <td>{{ row.income }}</td>
                  <td>{{ row.ecpm }}</td>
                  <td>{{ row.reqValue }}</td>
                  <td>{{ row.requests }}</td>
                  <td>{{ row.responseRate }}</td>
                  <td>{{ row.wins }}</td>
                  <td>{{ row.winRate }}</td>
                  <td>{{ row.impressions }}</td>
                  <td>{{ row.showRate }}</td>
                  <td>{{ row.clicks }}</td>
                  <td>{{ row.ctr }}</td>
                  <td>{{ row.cpc }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </section>

      <section v-else class="page">
        <section class="card card-soft ab-overview">
          <div class="card-header">
            <div class="section-title">A/B实验报表</div>
            <div class="section-inline">
              <button :class="['segmented-button', { active: abStatus === 'running' }]" type="button" @click="abStatus = 'running'">运行中A/B测试组</button>
              <button :class="['segmented-button', { active: abStatus === 'ended' }]" type="button" @click="abStatus = 'ended'">已结束A/B测试组</button>
            </div>
          </div>
          <div class="ab-toolbar">
            <label class="filter-item filter-item-stack">
              <span>流量分组</span>
              <div class="select-wrap select-inline"><select v-model="selectedExperimentId"><option v-for="item in visibleExperiments" :key="item.id" :value="item.id">{{ item.groupName }}</option></select></div>
            </label>
            <div class="ab-meta">
              <div>测试名称：{{ selectedExperiment.name }}</div>
              <div>生效时间：{{ selectedExperiment.range }}</div>
            </div>
            <span :class="['status-pill', selectedExperiment.status === 'running' ? 'status-pill-on' : 'status-pill-off']">{{ selectedExperiment.status === 'running' ? '运行中' : '已结束' }}</span>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <div class="section-title">A/B测试数据对比</div>
            <button class="outline-button" type="button" @click="exportTable(selectedExperiment.compareRows, 'AB测试对比')">导出</button>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>组别</th>
                  <th>千人均收益</th>
                  <th>预估收入</th>
                  <th>eCPM</th>
                  <th>千次请求价值</th>
                  <th>请求量</th>
                  <th>返回率</th>
                  <th>竞价成功数</th>
                  <th>竞价成功率</th>
                  <th>展示量</th>
                  <th>竞胜展示率</th>
                  <th>点击数</th>
                  <th>点击率</th>
                  <th>cpc</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in selectedExperiment.compareRows" :key="row.group">
                  <td>{{ row.group }}</td>
                  <td>{{ row.rpm }}</td>
                  <td>{{ row.income }}</td>
                  <td>{{ row.ecpm }}</td>
                  <td>{{ row.reqValue }}</td>
                  <td>{{ row.requests }}</td>
                  <td>{{ row.responseRate }}</td>
                  <td>{{ row.wins }}</td>
                  <td>{{ row.winRate }}</td>
                  <td>{{ row.impressions }}</td>
                  <td>{{ row.showRate }}</td>
                  <td>{{ row.clicks }}</td>
                  <td>{{ row.ctr }}</td>
                  <td>{{ row.cpc }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <div class="section-title">A/B测试图表</div>
            <div class="section-inline">
              <div class="select-wrap select-inline"><select v-model="abMetric"><option v-for="item in reportMetricOptions" :key="item.key" :value="item.key">{{ item.label }}</option></select></div>
              <span class="footer-note">{{ selectedExperiment.rangeShort }}</span>
            </div>
          </div>
          <div class="chart-panel">
            <svg class="line-chart" viewBox="0 0 780 260" preserveAspectRatio="none">
              <line v-for="tick in 5" :key="tick" :x1="40" :x2="750" :y1="25 + (tick - 1) * 50" :y2="25 + (tick - 1) * 50" class="chart-grid" />
              <polyline :points="abChartPoints.control" class="chart-line chart-line-alt" />
              <polyline :points="abChartPoints.test" class="chart-line" />
              <circle v-for="point in abChartCircles.control" :key="`c-${point.x}`" :cx="point.x" :cy="point.y" r="4" class="chart-dot chart-dot-alt" />
              <circle v-for="point in abChartCircles.test" :key="`t-${point.x}`" :cx="point.x" :cy="point.y" r="4" class="chart-dot" />
            </svg>
            <div class="chart-axis">
              <span v-for="row in selectedExperiment.detailRows" :key="row.date">{{ row.date }}</span>
            </div>
            <div class="chart-legend">
              <span><i class="legend-dot legend-dot-alt"></i>A对照组</span>
              <span><i class="legend-dot"></i>B测试组</span>
            </div>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <div class="section-title">数据明细 - {{ metricLabel(abMetric) }}</div>
            <button class="outline-button" type="button" @click="exportTable(selectedExperiment.detailRows, 'AB测试明细')">导出</button>
          </div>
          <div class="table-wrap">
            <table class="table-compact">
              <thead>
                <tr>
                  <th>日期</th>
                  <th>A对照组</th>
                  <th>B测试组</th>
                  <th>对比涨幅</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in selectedExperiment.detailRows" :key="row.date">
                  <td>{{ row.date }}</td>
                  <td>{{ row.control[abMetric] }}</td>
                  <td>{{ row.test[abMetric] }}</td>
                  <td :class="['diff-text', row.diffValue[abMetric] < 0 ? 'down' : 'up']">{{ row.diff[abMetric] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </section>
    </main>

    <div v-if="menuState.open" class="menu-mask" @click="closeGroupMenu">
      <div class="menu-panel" :style="menuStyle" @click.stop>
        <button type="button" @click="editGroupFromMenu">编辑分组</button>
        <button type="button" @click="duplicateGroupFromMenu">复制分组</button>
        <button :disabled="currentGroups.length === 1" type="button" @click="askDeleteGroup">删除分组</button>
      </div>
    </div>

    <BaseModal
      v-if="modalState === 'group'"
      title="分组配置"
      description="支持维护分组名称、优先级、广告位和命中规则。提交后会立即刷新当前表格。"
      @close="closeModal"
    >
      <form class="form-grid" @submit.prevent="submitGroupForm">
        <label class="form-block">
          <span class="form-label"><span class="required">分组名称</span><span class="helper">{{ groupForm.name.length }}/20</span></span>
          <input v-model="groupForm.name" class="text-input" maxlength="20" placeholder="请输入分组名称" />
        </label>

        <label class="form-block">
          <span class="form-label"><span class="required">优先级</span></span>
          <input v-model.number="groupForm.priority" class="number-input" min="1" max="99" type="number" />
        </label>

        <label class="form-block">
          <span class="form-label"><span>广告场景</span></span>
          <input :value="state.filters.scene" class="text-input" disabled />
        </label>

        <label class="form-block">
          <span class="form-label"><span>平台</span></span>
          <input :value="state.filters.platform" class="text-input" disabled />
        </label>

        <label class="form-block full">
          <span class="form-label"><span class="required">广告位</span></span>
          <div class="select-wrap">
            <select v-model="groupForm.slot">
              <option v-for="slot in currentSlots" :key="slot" :value="slot">{{ slot }}</option>
            </select>
          </div>
        </label>

        <label class="form-block full">
          <span class="form-label"><span>备注</span><span class="helper">可选</span></span>
          <textarea v-model="groupForm.note" placeholder="例如：命中高活跃 / 大盘回收 / 品牌优先"></textarea>
        </label>

        <div class="form-block full">
          <span class="form-label"><span>分组规则</span><button class="outline-button" type="button" @click="appendRule">添加规则</button></span>
          <div class="rules-editor">
            <div v-for="rule in groupForm.rules" :key="rule.id" class="rule-item">
              <input v-model="rule.field" class="text-input" placeholder="规则字段" />
              <input v-model="rule.operator" class="text-input" placeholder="运算符" />
              <input v-model="rule.value" class="text-input" placeholder="规则值" />
              <button class="danger-button" type="button" @click="removeRule(rule.id)">删除</button>
            </div>
          </div>
        </div>

        <div class="modal-footer full">
          <button class="ghost-button" type="button" @click="closeModal">取消</button>
          <button class="brand-button" type="submit">提交</button>
        </div>
      </form>
    </BaseModal>

    <BaseModal
      v-if="modalState === 'ab'"
      title="创建A/B测试"
      description="基于当前分组快速生成一个实验分组，用于价格、规则或流量占比验证。"
      @close="closeModal"
    >
      <form class="ab-layout" @submit.prevent="submitAbForm">
        <div class="form-grid single-column">
          <label class="form-block">
            <span class="form-label"><span class="required">实验名称</span></span>
            <input v-model="abForm.name" class="text-input" maxlength="20" />
          </label>

          <div class="inline-fields">
            <label class="form-block">
              <span class="form-label"><span class="required">实验流量占比</span></span>
              <input v-model.number="abForm.traffic" class="number-input" max="90" min="1" type="number" />
            </label>

            <label class="form-block">
              <span class="form-label"><span class="required">优先级</span></span>
              <input v-model.number="abForm.priority" class="number-input" max="99" min="1" type="number" />
            </label>
          </div>

          <label class="form-block">
            <span class="form-label"><span>实验说明</span></span>
            <textarea v-model="abForm.note"></textarea>
          </label>
        </div>

        <div class="ab-preview">
          <div class="ab-badge">实验预览</div>
          <h4>{{ currentGroup.name }}</h4>
          <div class="helper">当前广告位：{{ currentGroup.slot }}</div>
          <div class="stats-panel">
            <div class="stats-card"><div class="label">当前PID数</div><strong>{{ currentGroup.pids.length }}</strong></div>
            <div class="stats-card"><div class="label">启用PID数</div><strong>{{ enabledCount }}</strong></div>
            <div class="stats-card"><div class="label">当前优先级</div><strong>{{ currentGroup.priority }}</strong></div>
          </div>
        </div>

        <div class="modal-footer ab-footer">
          <button class="ghost-button" type="button" @click="closeModal">取消</button>
          <button class="brand-button" type="submit">生成实验组</button>
        </div>
      </form>
    </BaseModal>

    <BaseModal
      v-if="modalState === 'pid'"
      :title="editingPidId ? '编辑PID' : '添加PID'"
      description="选择 DSP 来源后继承模板指标，只需绑定 PID 并设置状态。"
      @close="closeModal"
    >
      <form class="form-grid single-column" @submit.prevent="submitPidForm">
        <label class="form-block">
          <span class="form-label"><span class="required">DSP来源</span></span>
          <div class="select-wrap">
            <select v-model="pidForm.templateName" :disabled="!!editingPidId">
              <option value="" disabled>请选择DSP来源</option>
              <option v-for="item in dspCatalog" :key="item.name" :value="item.name">{{ item.name }}</option>
            </select>
          </div>
        </label>

        <label class="form-block">
          <span class="form-label"><span class="required">PID</span></span>
          <input v-model="pidForm.pidCode" class="text-input" placeholder="请输入PID" />
        </label>

        <div class="stats-panel pid-bind-grid">
          <div class="stats-card">
            <div class="label">广告场景</div>
            <strong>{{ currentGroup.scene }}</strong>
          </div>
          <div class="stats-card">
            <div class="label">平台</div>
            <strong>{{ currentGroup.platform }}</strong>
          </div>
          <div class="stats-card">
            <div class="label">广告位</div>
            <strong>{{ currentGroup.slot }}</strong>
          </div>
          <div class="stats-card">
            <div class="label">绑定分组</div>
            <strong>{{ currentGroup.name }}</strong>
          </div>
        </div>

        <div v-if="selectedPidTemplate" class="stats-panel pid-bind-grid">
          <div class="stats-card">
            <div class="label">模板价格</div>
            <strong>{{ formatMetric(selectedPidTemplate.price, 'currency') }}</strong>
          </div>
          <div class="stats-card">
            <div class="label">预估收入</div>
            <strong>{{ formatMetric(selectedPidTemplate.estimatedRevenue, 'number') }}</strong>
          </div>
          <div class="stats-card">
            <div class="label">eCPM</div>
            <strong>{{ formatMetric(selectedPidTemplate.ecpm, 'currency') }}</strong>
          </div>
          <div class="stats-card">
            <div class="label">请求量</div>
            <strong>{{ formatMetric(selectedPidTemplate.requestVolume, 'volume') }}</strong>
          </div>
        </div>

        <label class="form-block">
          <span class="form-label"><span>启用状态</span></span>
          <div class="select-wrap">
            <select v-model="pidEnabledString">
              <option value="true">启用</option>
              <option value="false">停用</option>
            </select>
          </div>
        </label>

        <div class="modal-footer full">
          <button v-if="editingPidId" class="danger-button" type="button" @click="askDeletePid">删除PID</button>
          <button class="ghost-button" type="button" @click="closeModal">取消</button>
          <button class="brand-button" type="submit">提交</button>
        </div>
      </form>
    </BaseModal>

    <BaseModal v-if="modalState === 'price'" title="修改价格" :description="priceDescription" size="narrow" @close="closeModal">
      <form class="form-grid single-column" @submit.prevent="submitPriceForm">
        <label class="form-block">
          <span class="form-label"><span class="required">价格</span></span>
          <input v-model.number="priceForm.price" class="number-input" min="0" step="0.01" type="number" />
        </label>

        <div class="modal-footer full">
          <button class="ghost-button" type="button" @click="closeModal">取消</button>
          <button class="brand-button" type="submit">保存</button>
        </div>
      </form>
    </BaseModal>

    <BaseModal v-if="confirmState.open" :title="confirmState.title" :description="confirmState.content" size="narrow" @close="closeConfirm">
      <div class="modal-footer confirm-only">
        <button class="ghost-button" type="button" @click="closeConfirm">取消</button>
        <button :class="confirmState.danger ? 'danger-button' : 'brand-button'" type="button" @click="confirmAction">{{ confirmState.confirmText }}</button>
      </div>
    </BaseModal>

    <div class="toast-stack">
      <div v-for="toast in toasts" :key="toast.id" :class="['toast', toast.type]">{{ toast.message }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import BaseModal from './BaseModal.vue'
import { metricColumns, useTrafficGroupManager } from '../composables/useTrafficGroupManager'

const primaryMenus = [
  '广告交互管理',
  '品牌管理',
  '品牌小工具',
  '柚+管理',
  '女人通管理',
  '女人通消费管理',
  '女人通数据管理',
  '媒体数据管理',
  'DSP数据管理',
  'MARKETING API管理',
  '第三方DMP管理',
  '小工具'
]

const pageMenus = [
  { key: 'group', label: '流量分组管理' },
  { key: 'pid', label: 'PID管理' },
  { key: 'report', label: '综合报表' },
  { key: 'ab', label: 'A/B测试报表' }
]

const scenes = ['开屏', '信息流']
const platforms = ['iOS', 'Android']
const currentPage = ref('group')

const {
  state,
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
} = useTrafficGroupManager()

const modalState = ref('')
const editingGroupId = ref('')
const editingPidId = ref('')
const editingPricePidId = ref('')

const groupForm = reactive(createGroupForm())
const abForm = reactive(createAbForm())
const pidForm = reactive(createPidForm())
const priceForm = reactive({ price: 0 })

const menuState = reactive({ open: false, x: 0, y: 0, groupId: '' })
const confirmState = reactive({ open: false, title: '', content: '', confirmText: '确定', danger: false, action: null })
const toasts = ref([])

const pidFilters = reactive({ scene: '全部场景', platform: '全部平台', slot: '全部广告位' })
const pidPage = ref(1)
const pageSize = 10
const reportFilters = reactive({ start: '2026-05-25', end: '2026-06-01', scene: '全部', platform: '全部', group: '全部分组' })
const reportMetric = ref('incomeValue')
const abMetric = ref('rpm')
const abStatus = ref('running')

const reportMetricOptions = [
  { key: 'rpmValue', label: '千人均收益' },
  { key: 'incomeValue', label: '预估收入' },
  { key: 'ecpmValue', label: 'eCPM' },
  { key: 'reqValueValue', label: '千次请求价值' }
]

const reportRows = ref(buildReportRows())
const experiments = ref(buildExperiments())
const selectedExperimentId = ref(experiments.value[0].id)

const currentPageLabel = computed(() => pageMenus.find(item => item.key === currentPage.value)?.label || '流量分组管理')
const enabledCount = computed(() => currentGroup.value.pids.filter(pid => pid.enabled).length)
const groupMeta = computed(() => `优先级 ${currentGroup.value.priority} · ${enabledCount.value}/${currentGroup.value.pids.length} 个DSP来源启用 · ${currentGroup.value.note || '未填写备注'}`)
const pidEnabledString = computed({
  get: () => String(pidForm.enabled),
  set: value => {
    pidForm.enabled = value === 'true'
  }
})
const menuStyle = computed(() => ({ left: `${menuState.x}px`, top: `${menuState.y}px` }))
const priceDescription = computed(() => editingPricePidId.value ? findPid(editingPricePidId.value)?.name || '' : '')
const pidSlotOptions = computed(() => Array.from(new Set(allPidRows.value.map(item => item.slot))))
const reportGroupOptions = computed(() => Array.from(new Set(allPidRows.value.map(item => item.groupName))))
const selectedPidTemplate = computed(() => dspCatalog.value.find(item => item.name === pidForm.templateName) || null)

const allPidRows = computed(() => {
  return Object.values(state.datasets).flatMap(dataset => {
    return dataset.groups.flatMap(group => {
      return group.pids.map((pid, index) => ({
        rowKey: `${group.id}-${pid.id}`,
        id: pid.id,
        pid: pid.pidCode || `PID-${String(index + 1).padStart(4, '0')}`,
        name: pid.name,
        enabled: pid.enabled,
        platform: group.platform,
        scene: group.scene,
        slot: group.slot,
        groupId: group.id,
        groupName: group.name,
        datasetKey: `${group.scene}|${group.platform}`
      }))
    })
  })
})

const filteredPidRows = computed(() => {
  return allPidRows.value.filter(row => {
    if (pidFilters.scene !== '全部场景' && row.scene !== pidFilters.scene) return false
    if (pidFilters.platform !== '全部平台' && row.platform !== pidFilters.platform) return false
    if (pidFilters.slot !== '全部广告位' && row.slot !== pidFilters.slot) return false
    return true
  })
})

const pidPageCount = computed(() => Math.max(1, Math.ceil(filteredPidRows.value.length / pageSize)))
const pagedPidRows = computed(() => {
  const start = (pidPage.value - 1) * pageSize
  return filteredPidRows.value.slice(start, start + pageSize)
})

const reportSummary = computed(() => ({
  rpm: '121.31',
  income: '3,070,285.75',
  ecpm: '9.32',
  reqValue: '102.73',
  requests: '27,603,716',
  responseRate: '81.86%',
  wins: '16,586,484',
  winRate: '75.25%',
  impressions: '12,304,300',
  showRate: '70.80%',
  clicks: '83,698',
  ctr: '0.56%',
  cpc: '2.18'
}))

const reportChartPoints = computed(() => buildLinePoints(reportRows.value.map(item => item[reportMetric.value])))
const reportChartCircles = computed(() => buildLineCircles(reportRows.value.map(item => item[reportMetric.value])))
const visibleExperiments = computed(() => experiments.value.filter(item => item.status === abStatus.value))
const selectedExperiment = computed(() => visibleExperiments.value.find(item => item.id === selectedExperimentId.value) || visibleExperiments.value[0])
const abChartPoints = computed(() => buildDualChartPoints(selectedExperiment.value.detailRows, abMetric.value))
const abChartCircles = computed(() => buildDualChartCircles(selectedExperiment.value.detailRows, abMetric.value))

watch([() => pidFilters.scene, () => pidFilters.platform, () => pidFilters.slot], () => {
  pidPage.value = 1
})

watch(visibleExperiments, value => {
  if (!value.some(item => item.id === selectedExperimentId.value)) {
    selectedExperimentId.value = value[0]?.id || ''
  }
}, { immediate: true })

function sortIndicator(key) {
  if (state.sort.key !== key) {
    return '▲'
  }
  return state.sort.direction === 'asc' ? '▲' : '▼'
}

function formatMetric(value, type) {
  const number = Number(value) || 0
  if (type === 'currency') {
    return `¥${number.toFixed(2)}`
  }
  if (type === 'percent') {
    return `${number.toFixed(1)}%`
  }
  if (type === 'volume') {
    return number >= 10000 ? `${round(number / 10000, 1)}万` : number.toLocaleString('zh-CN')
  }
  return number.toLocaleString('zh-CN', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
}

function metricLabel(key) {
  return reportMetricOptions.find(item => item.key === key)?.label || '指标'
}

function buildLinePoints(values) {
  const points = buildPointSeries(values)
  return points.map(point => `${point.x},${point.y}`).join(' ')
}

function buildLineCircles(values) {
  return buildPointSeries(values)
}

function buildDualChartPoints(rows, key) {
  const controlValues = rows.map(row => row.controlValue[key])
  const testValues = rows.map(row => row.testValue[key])
  return {
    control: buildLinePoints(controlValues),
    test: buildLinePoints(testValues)
  }
}

function buildDualChartCircles(rows, key) {
  const controlValues = rows.map(row => row.controlValue[key])
  const testValues = rows.map(row => row.testValue[key])
  return {
    control: buildLineCircles(controlValues),
    test: buildLineCircles(testValues)
  }
}

function buildPointSeries(values) {
  const max = Math.max(...values)
  const min = Math.min(...values)
  const span = max - min || 1
  return values.map((value, index) => ({
    x: 40 + (710 / Math.max(values.length - 1, 1)) * index,
    y: 225 - ((value - min) / span) * 170
  }))
}

function exportTable(rows, filename) {
  const content = JSON.stringify(rows, null, 2)
  const blob = new Blob([content], { type: 'application/json;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${filename}.json`
  link.click()
  URL.revokeObjectURL(url)
  pushToast(`${filename} 已导出`, 'success')
}

function openPidFromList(row) {
  state.filters.scene = row.scene
  state.filters.platform = row.platform
  switchGroup(row.groupId)
  currentPage.value = 'pid'
  openPidModal(row.id)
}

function togglePidFromList(row) {
  state.filters.scene = row.scene
  state.filters.platform = row.platform
  switchGroup(row.groupId)
  togglePidEnabledWithToast(row.id)
}

function openGroupMenu(groupId, event) {
  const rect = event.currentTarget.getBoundingClientRect()
  menuState.open = true
  menuState.groupId = groupId
  menuState.x = Math.max(12, rect.left - 96)
  menuState.y = rect.bottom + 8
}

function closeGroupMenu() {
  menuState.open = false
  menuState.groupId = ''
}

function openGroupModal(groupId = '') {
  closeGroupMenu()
  editingGroupId.value = groupId
  Object.assign(groupForm, createGroupForm(groupId ? currentGroups.value.find(group => group.id === groupId) : null, currentSlots.value[0]))
  modalState.value = 'group'
}

function openAbModal() {
  Object.assign(abForm, createAbForm(currentGroup.value))
  modalState.value = 'ab'
}

function openPidModal(pidId = '') {
  editingPidId.value = pidId
  Object.assign(pidForm, createPidForm(pidId ? findPid(pidId) : null))
  modalState.value = 'pid'
}

function openPriceModal(pidId) {
  editingPricePidId.value = pidId
  priceForm.price = findPid(pidId)?.price || 0
  modalState.value = 'price'
}

function closeModal() {
  modalState.value = ''
  editingGroupId.value = ''
  editingPidId.value = ''
  editingPricePidId.value = ''
}

function appendRule() {
  groupForm.rules.push(createRule())
}

function removeRule(ruleId) {
  groupForm.rules = groupForm.rules.filter(rule => rule.id !== ruleId)
}

function submitGroupForm() {
  if (!groupForm.name.trim()) {
    pushToast('请先填写分组名称', 'error')
    return
  }

  upsertGroup({
    name: groupForm.name,
    priority: groupForm.priority,
    slot: groupForm.slot,
    note: groupForm.note,
    rules: groupForm.rules
  }, editingGroupId.value)

  const editing = !!editingGroupId.value
  closeModal()
  pushToast(editing ? '分组已更新' : '分组已创建', 'success')
}

function submitAbForm() {
  if (!abForm.name.trim()) {
    pushToast('请填写实验名称', 'error')
    return
  }
  createAbGroup(abForm)
  experiments.value.unshift(createExperimentFromCurrentGroup(abForm.name))
  closeModal()
  pushToast('A/B测试分组已创建', 'success')
}

function submitPidForm() {
  if (!pidForm.templateName.trim()) {
    pushToast('请选择DSP来源', 'error')
    return
  }

  if (!pidForm.pidCode.trim()) {
    pushToast('请填写PID', 'error')
    return
  }

  const editing = !!editingPidId.value
  upsertPid({
    ...pidForm,
    name: pidForm.templateName,
    templateName: pidForm.templateName
  }, editingPidId.value)
  closeModal()
  pushToast(editing ? 'PID已更新' : 'PID已添加', 'success')
}

function submitPriceForm() {
  updatePrice(editingPricePidId.value, priceForm.price)
  closeModal()
  pushToast('价格已更新', 'success')
}

function toggleGroupEnabledWithToast() {
  const enabled = toggleGroupEnabled()
  pushToast(enabled ? '分组已启用' : '分组已停用', enabled ? 'success' : 'error')
}

function togglePidEnabledWithToast(pidId) {
  const pid = togglePidEnabled(pidId)
  pushToast(pid.enabled ? `${pid.name} 已启用` : `${pid.name} 已停用`, pid.enabled ? 'success' : 'error')
}

function editGroupFromMenu() {
  openGroupModal(menuState.groupId)
}

function duplicateGroupFromMenu() {
  duplicateGroup(menuState.groupId)
  closeGroupMenu()
  pushToast('分组已复制', 'success')
}

function askDeleteGroup() {
  const group = currentGroups.value.find(item => item.id === menuState.groupId)
  closeGroupMenu()
  openConfirm({
    title: '删除分组',
    content: `确认删除“${group.name}”吗？此操作会移除该分组下所有PID。`,
    confirmText: '删除',
    danger: true,
    action: () => {
      removeGroup(group.id)
      pushToast('分组已删除', 'success')
    }
  })
}

function askDeletePid() {
  const pid = findPid(editingPidId.value)
  openConfirm({
    title: '删除PID',
    content: `确认删除“${pid.name}”吗？`,
    confirmText: '删除',
    danger: true,
    action: () => {
      removePid(pid.id)
      closeModal()
      pushToast('PID已删除', 'success')
    }
  })
}

function openConfirm({ title, content, confirmText, danger, action }) {
  confirmState.open = true
  confirmState.title = title
  confirmState.content = content
  confirmState.confirmText = confirmText
  confirmState.danger = danger
  confirmState.action = action
}

function closeConfirm() {
  confirmState.open = false
  confirmState.title = ''
  confirmState.content = ''
  confirmState.confirmText = '确定'
  confirmState.danger = false
  confirmState.action = null
}

function confirmAction() {
  const action = confirmState.action
  closeConfirm()
  if (action) {
    action()
  }
}

function pushToast(message, type) {
  const id = `${Date.now()}-${Math.random()}`
  toasts.value.push({ id, message, type })
  window.setTimeout(() => {
    toasts.value = toasts.value.filter(item => item.id !== id)
  }, 2200)
}

function createGroupForm(group = null, defaultSlot = currentSlots.value?.[0] || '') {
  return {
    name: group?.name || '',
    priority: group?.priority || currentGroups.value.length + 1,
    slot: group?.slot || defaultSlot,
    note: group?.note || '',
    rules: (group?.rules || [createRule('用户标签', '等于', '全部用户')]).map(rule => createRule(rule.field, rule.operator, rule.value))
  }
}

function createRule(field = '用户标签', operator = '等于', value = '全部用户') {
  return { id: `${Date.now()}-${Math.random()}`, field, operator, value }
}

function createAbForm(group = currentGroup.value) {
  return {
    name: `${group.name}-AB测试`,
    traffic: 30,
    priority: group.priority + 1,
    note: `基于 ${group.name} 复制，保留原有PID并支持后续单独编辑。`
  }
}

function createPidForm(pid = null) {
  return {
    templateName: pid?.name || '',
    name: pid?.name || '',
    pidCode: pid?.pidCode || '',
    price: pid?.price || 12.5,
    statusColor: pid?.statusColor || 'green',
    enabled: pid?.enabled ?? true,
    estimatedRevenue: pid?.estimatedRevenue || 8200,
    profitPerMille: pid?.profitPerMille || 0.08,
    ecpm: pid?.ecpm || 16.4,
    requestValue: pid?.requestValue || 0.61,
    requestVolume: pid?.requestVolume || 64000,
    returnRate: pid?.returnRate || 52.4,
    bidSuccessCount: pid?.bidSuccessCount || 16000,
    bidSuccessRate: pid?.bidSuccessRate || 38.5,
    impressionCount: pid?.impressionCount || 31000,
    winRate: pid?.winRate || 74.2,
    clickRate: pid?.clickRate || 2.8,
    cpc: pid?.cpc || 0.86
  }
}

function buildReportRows() {
  return [
    { date: '2026-05-25', rpm: '118.44', rpmValue: 118.44, income: '377,610.22', incomeValue: 377610.22, ecpm: '8.72', ecpmValue: 8.72, reqValue: '95.62', reqValueValue: 95.62, requests: '3,502,114', responseRate: '83.12%', wins: '2,146,251', winRate: '76.34%', impressions: '1,504,236', showRate: '70.08%', clicks: '10,241', ctr: '0.68%', cpc: '2.11' },
    { date: '2026-05-26', rpm: '119.38', rpmValue: 119.38, income: '382,714.47', incomeValue: 382714.47, ecpm: '8.95', ecpmValue: 8.95, reqValue: '97.80', reqValueValue: 97.8, requests: '3,611,702', responseRate: '82.76%', wins: '2,181,430', winRate: '75.93%', impressions: '1,532,843', showRate: '70.27%', clicks: '10,462', ctr: '0.68%', cpc: '2.13' },
    { date: '2026-05-27', rpm: '120.02', rpmValue: 120.02, income: '386,823.31', incomeValue: 386823.31, ecpm: '9.08', ecpmValue: 9.08, reqValue: '99.15', reqValueValue: 99.15, requests: '3,432,847', responseRate: '81.42%', wins: '2,075,398', winRate: '75.61%', impressions: '1,498,207', showRate: '72.19%', clicks: '10,095', ctr: '0.67%', cpc: '2.16' },
    { date: '2026-05-28', rpm: '121.57', rpmValue: 121.57, income: '388,354.78', incomeValue: 388354.78, ecpm: '9.27', ecpmValue: 9.27, reqValue: '103.42', reqValueValue: 103.42, requests: '3,385,604', responseRate: '80.55%', wins: '2,022,450', winRate: '75.14%', impressions: '1,492,830', showRate: '73.81%', clicks: '10,288', ctr: '0.69%', cpc: '2.19' },
    { date: '2026-05-29', rpm: '122.08', rpmValue: 122.08, income: '389,870.15', incomeValue: 389870.15, ecpm: '9.36', ecpmValue: 9.36, reqValue: '104.67', reqValueValue: 104.67, requests: '3,429,008', responseRate: '81.03%', wins: '2,058,112', winRate: '75.88%', impressions: '1,515,220', showRate: '73.62%', clicks: '10,432', ctr: '0.69%', cpc: '2.17' },
    { date: '2026-05-30', rpm: '121.11', rpmValue: 121.11, income: '382,506.49', incomeValue: 382506.49, ecpm: '9.31', ecpmValue: 9.31, reqValue: '103.95', reqValueValue: 103.95, requests: '3,369,944', responseRate: '81.88%', wins: '2,027,926', winRate: '74.90%', impressions: '1,467,828', showRate: '72.38%', clicks: '10,079', ctr: '0.69%', cpc: '2.18' },
    { date: '2026-05-31', rpm: '123.02', rpmValue: 123.02, income: '380,765.62', incomeValue: 380765.62, ecpm: '9.49', ecpmValue: 9.49, reqValue: '105.24', reqValueValue: 105.24, requests: '3,332,791', responseRate: '82.51%', wins: '2,011,204', winRate: '75.77%', impressions: '1,459,973', showRate: '72.59%', clicks: '10,694', ctr: '0.73%', cpc: '2.12' },
    { date: '2026-06-01', rpm: '125.06', rpmValue: 125.06, income: '381,640.71', incomeValue: 381640.71, ecpm: '9.62', ecpmValue: 9.62, reqValue: '111.98', reqValueValue: 111.98, requests: '3,539,706', responseRate: '81.62%', wins: '2,063,713', winRate: '72.43%', impressions: '1,833,163', showRate: '69.90%', clicks: '11,407', ctr: '0.62%', cpc: '2.18' }
  ]
}

function buildExperiments() {
  return [
    {
      id: 'ab-running-1',
      status: 'running',
      groupName: '默认分组 vs AB实验组',
      name: '开屏价格调优实验',
      range: '2026-05-25 00:00 至 2026-06-01 23:59',
      rangeShort: '2026-05-25 至 2026-06-01',
      compareRows: [
        { group: 'A对照组', rpm: '128.34', income: '1,422,603.52', ecpm: '9.62', reqValue: '104.15', requests: '13,671,284', responseRate: '82.18%', wins: '8,214,510', winRate: '74.95%', impressions: '6,244,102', showRate: '71.22%', clicks: '41,002', ctr: '0.66%', cpc: '2.15' },
        { group: 'B测试组', rpm: '141.84', income: '1,566,430.77', ecpm: '10.08', reqValue: '112.67', requests: '13,898,104', responseRate: '83.11%', wins: '8,371,822', winRate: '75.94%', impressions: '6,451,860', showRate: '72.41%', clicks: '43,318', ctr: '0.67%', cpc: '2.21' }
      ],
      detailRows: buildExperimentDetailRows()
    },
    {
      id: 'ab-ended-1',
      status: 'ended',
      groupName: '信息流默认分组 vs AB实验组',
      name: '信息流回收实验',
      range: '2026-05-10 00:00 至 2026-05-17 23:59',
      rangeShort: '2026-05-10 至 2026-05-17',
      compareRows: [
        { group: 'A对照组', rpm: '112.14', income: '1,204,308.33', ecpm: '8.14', reqValue: '96.28', requests: '12,512,140', responseRate: '80.24%', wins: '7,101,325', winRate: '70.74%', impressions: '5,804,102', showRate: '68.90%', clicks: '37,204', ctr: '0.64%', cpc: '2.06' },
        { group: 'B测试组', rpm: '116.49', income: '1,250,147.22', ecpm: '8.51', reqValue: '98.80', requests: '12,653,729', responseRate: '81.02%', wins: '7,212,468', winRate: '71.80%', impressions: '5,932,441', showRate: '69.52%', clicks: '38,015', ctr: '0.64%', cpc: '2.08' }
      ],
      detailRows: buildExperimentDetailRows('ended')
    }
  ]
}

function buildExperimentDetailRows(mode = 'running') {
  const base = [
    ['2026-05-25', 144.31, 157.62],
    ['2026-05-26', 136.26, 166.14],
    ['2026-05-27', 121.89, 126.06],
    ['2026-05-28', 142.46, 149.16],
    ['2026-05-29', 141.71, 140.38],
    ['2026-05-30', 116.19, 113.49],
    ['2026-05-31', 121.45, 124.21],
    ['2026-06-01', 146.54, 153.69]
  ]
  return base.map(([date, controlRpm, testRpm], index) => {
    const controlIncome = mode === 'running' ? 175000 + index * 3600 : 152000 + index * 2800
    const testIncome = mode === 'running' ? controlIncome * (1 + (testRpm - controlRpm) / 220) : controlIncome * 1.04
    const controlEcpm = controlRpm / 13.6
    const testEcpm = testRpm / 13.6
    const controlReq = controlRpm / 1.36
    const testReq = testRpm / 1.36
    const diffRpmValue = round(((testRpm - controlRpm) / controlRpm) * 100, 2)
    const diffIncomeValue = round(((testIncome - controlIncome) / controlIncome) * 100, 2)
    const diffEcpmValue = round(((testEcpm - controlEcpm) / controlEcpm) * 100, 2)
    const diffReqValue = round(((testReq - controlReq) / controlReq) * 100, 2)

    return {
      date,
      control: {
        rpmValue: controlRpm.toFixed(2),
        incomeValue: controlIncome.toFixed(2),
        ecpmValue: controlEcpm.toFixed(2),
        reqValueValue: controlReq.toFixed(2),
        rpm: controlRpm.toFixed(2),
        income: controlIncome.toFixed(2),
        ecpm: controlEcpm.toFixed(2),
        reqValue: controlReq.toFixed(2)
      },
      test: {
        rpmValue: testRpm.toFixed(2),
        incomeValue: testIncome.toFixed(2),
        ecpmValue: testEcpm.toFixed(2),
        reqValueValue: testReq.toFixed(2),
        rpm: testRpm.toFixed(2),
        income: testIncome.toFixed(2),
        ecpm: testEcpm.toFixed(2),
        reqValue: testReq.toFixed(2)
      },
      diff: {
        rpmValue: signedPercent(diffRpmValue),
        incomeValue: signedPercent(diffIncomeValue),
        ecpmValue: signedPercent(diffEcpmValue),
        reqValueValue: signedPercent(diffReqValue),
        rpm: signedPercent(diffRpmValue),
        income: signedPercent(diffIncomeValue),
        ecpm: signedPercent(diffEcpmValue),
        reqValue: signedPercent(diffReqValue)
      },
      controlValue: { rpm: controlRpm, incomeValue: controlIncome, ecpmValue: controlEcpm, reqValueValue: controlReq, rpmValue: controlRpm },
      testValue: { rpm: testRpm, incomeValue: testIncome, ecpmValue: testEcpm, reqValueValue: testReq, rpmValue: testRpm },
      diffValue: { rpm: diffRpmValue, incomeValue: diffIncomeValue, ecpmValue: diffEcpmValue, reqValueValue: diffReqValue, rpmValue: diffRpmValue }
    }
  })
}

function createExperimentFromCurrentGroup(name) {
  return {
    id: `ab-${Date.now()}`,
    status: 'running',
    groupName: `${currentGroup.value.name} vs 新实验组`,
    name,
    range: '2026-06-01 00:00 至 2026-06-08 23:59',
    rangeShort: '2026-06-01 至 2026-06-08',
    compareRows: [
      { group: 'A对照组', rpm: '132.41', income: '1,120,442.12', ecpm: '9.04', reqValue: '101.12', requests: '10,845,003', responseRate: '82.02%', wins: '6,444,102', winRate: '74.12%', impressions: '4,982,241', showRate: '71.24%', clicks: '30,442', ctr: '0.61%', cpc: '2.09' },
      { group: 'B测试组', rpm: '139.24', income: '1,189,206.55', ecpm: '9.36', reqValue: '107.55', requests: '11,054,883', responseRate: '82.74%', wins: '6,632,184', winRate: '74.96%', impressions: '5,104,228', showRate: '71.91%', clicks: '31,208', ctr: '0.61%', cpc: '2.14' }
    ],
    detailRows: buildExperimentDetailRows()
  }
}

function signedPercent(value) {
  const prefix = value > 0 ? '+' : ''
  return `${prefix}${value.toFixed(2)}%`
}

function round(value, digits = 1) {
  const factor = 10 ** digits
  return Math.round(Number(value) * factor) / factor
}
</script>

<style scoped>
:global(body) {
  margin: 0;
  background: #f5f6fa;
  color: #1f2430;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

:global(*) {
  box-sizing: border-box;
}

.traffic-app {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 224px 1fr;
  --line: #e8e8ef;
  --brand: #e24b8d;
  --muted: #83889a;
  --shadow: 0 12px 30px rgba(28, 32, 45, 0.08);
}

.sidebar {
  background: #fff;
  border-right: 1px solid var(--line);
}

.brand {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  border-bottom: 1px solid var(--line);
  font-size: 18px;
  font-weight: 600;
}

.brand-badge,
.nav-icon,
.crumb-sep,
.metric-tip,
.chip-dot,
.edit-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.brand-badge {
  width: 18px;
  height: 18px;
  border: 2px solid #2f3444;
  border-radius: 4px;
  font-size: 11px;
}

.nav-list {
  padding: 8px;
  display: grid;
  gap: 2px;
}

.nav-item,
.nav-subitem {
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 12px 10px;
  border: none;
  border-radius: 12px;
  color: #1f2430;
  background: none;
  text-align: left;
  cursor: pointer;
}

.nav-item.active,
.nav-subitem.active {
  color: var(--brand);
  background: linear-gradient(90deg, rgba(226, 75, 141, 0.08), rgba(226, 75, 141, 0));
}

.nav-item.active::before,
.nav-subitem.active::before {
  content: '';
  position: absolute;
  left: 0;
  width: 3px;
  height: 26px;
  border-radius: 999px;
  background: var(--brand);
}

.nav-main {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-icon {
  width: 14px;
  height: 14px;
  border: 1.6px solid currentColor;
  border-radius: 2px;
}

.nav-arrow {
  color: #99a1b3;
}

.nav-sublist {
  padding-left: 12px;
}

.nav-subitem {
  padding-left: 32px;
}

.content {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 26px;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(10px);
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--muted);
  font-size: 14px;
}

.breadcrumbs strong {
  color: #1f2430;
  font-weight: 500;
}

.crumb-sep {
  width: 6px;
  height: 6px;
  border-top: 1.5px solid #a2a6b3;
  border-right: 1.5px solid #a2a6b3;
  transform: rotate(45deg);
}

.page {
  padding: 18px 24px 30px;
  display: grid;
  gap: 20px;
}

.card {
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: #fff;
  box-shadow: var(--shadow);
}

.card-soft {
  padding: 16px 18px;
}

.filter-bar,
.group-row,
.field-inline,
.modal-footer,
.inline-fields,
.toast-stack,
.section-inline,
.table-actions,
.chart-legend,
.ab-toolbar,
.date-range,
.pager {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-block {
  overflow: visible;
}

.filter-grid {
  display: grid;
  gap: 16px;
  align-items: end;
}

.pid-filter-grid {
  grid-template-columns: repeat(3, minmax(0, 220px)) 120px;
}

.report-filter-grid {
  grid-template-columns: minmax(320px, 420px) repeat(3, minmax(0, 180px)) 120px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666b7b;
}

.filter-item-stack {
  align-items: flex-start;
  flex-direction: column;
  gap: 8px;
}

.filter-wide {
  min-width: 0;
}

.filter-action {
  display: flex;
  align-items: flex-end;
}

.select-wrap {
  position: relative;
}

.select-wrap::after {
  content: '▾';
  position: absolute;
  top: 50%;
  right: 14px;
  transform: translateY(-50%);
  font-size: 12px;
  color: #a4a9b7;
  pointer-events: none;
}

select,
.text-input,
.number-input,
textarea,
input[type='date'] {
  min-height: 36px;
  min-width: 112px;
  padding: 0 38px 0 14px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #fff;
  color: #1f2430;
  outline: none;
}

input[type='date'] {
  padding-right: 14px;
}

textarea {
  min-height: 84px;
  padding: 10px 14px;
  resize: vertical;
}

.select-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-width: 108px;
  height: 36px;
  padding: 0 38px 0 14px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 4px 12px rgba(40, 44, 58, 0.04);
}

.chip-select {
  min-width: 68px;
  border: none;
  padding: 0 18px 0 0;
  box-shadow: none;
}

.select-inline select {
  min-width: 160px;
}

.chip-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #7a4bf2;
  box-shadow: 0 0 0 4px rgba(122, 75, 242, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid var(--line);
}

.tight {
  padding-bottom: 12px;
}

.outline-button,
.ghost-button,
.danger-button,
.brand-button,
.icon-button,
.tiny-button,
.edit-link,
.sortable,
.segmented-button {
  cursor: pointer;
}

.outline-button,
.ghost-button,
.danger-button,
.segmented-button {
  min-height: 34px;
  padding: 0 15px;
  border: 1px solid rgba(226, 75, 141, 0.45);
  border-radius: 12px;
  background: #fff;
  color: var(--brand);
}

.brand-button {
  min-height: 38px;
  padding: 0 18px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--brand), #f26fa7);
  color: #fff;
}

.segmented-button.active {
  background: linear-gradient(135deg, rgba(226, 75, 141, 0.14), rgba(226, 75, 141, 0.04));
}

.danger-button {
  color: #ef5350;
  border-color: rgba(239, 83, 80, 0.3);
}

.plus {
  margin-right: 6px;
  font-size: 20px;
  line-height: 1;
}

.group-tabs {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding: 0 16px;
  border-bottom: 1px solid var(--line);
  background: linear-gradient(180deg, #fff, #fff8fc);
}

.group-tab {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 52px;
  padding: 0 2px;
  border: none;
  background: none;
  color: #7d7483;
}

.group-tab.active {
  color: var(--brand);
  font-weight: 600;
}

.group-tab.active::after {
  content: '';
  position: absolute;
  right: 0;
  bottom: -1px;
  left: 0;
  height: 2px;
  border-radius: 999px;
  background: var(--brand);
}

.group-body {
  display: grid;
  gap: 16px;
  padding: 14px 16px 18px;
  background: #fcfcff;
}

.tag,
.ab-badge,
.status-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
}

.tag {
  min-height: 28px;
  padding: 0 10px;
  border: 1px solid rgba(55, 115, 215, 0.18);
  background: rgba(55, 115, 215, 0.08);
  color: #3773d7;
}

.ab-badge {
  height: 28px;
  padding: 0 10px;
  background: rgba(226, 75, 141, 0.12);
  color: var(--brand);
  font-size: 13px;
}

.badge-inline {
  height: 22px;
  font-size: 12px;
}

.status-pill {
  min-height: 28px;
  padding: 0 12px;
  font-size: 12px;
  justify-content: center;
}

.status-pill-on {
  color: #23945b;
  background: #eefbf3;
}

.status-pill-off {
  color: #d25959;
  background: #fff4f4;
}

.footer-note,
.helper {
  color: #9aa0af;
  font-size: 12px;
}

.rules-list,
.rules-editor,
.form-grid,
.stats-panel {
  display: grid;
  gap: 12px;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 10px;
  border: 1px dashed #d9dce8;
  border-radius: 12px;
  background: #fafbff;
}

.form-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.single-column {
  grid-template-columns: 1fr;
}

.form-block {
  display: grid;
  gap: 8px;
}

.full {
  grid-column: 1 / -1;
}

.form-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #525a6d;
  font-size: 14px;
}

.required::before {
  content: '*';
  margin-right: 4px;
  color: var(--brand);
}

.switch {
  position: relative;
  width: 32px;
  height: 20px;
  border: none;
  border-radius: 999px;
  background: #cad0db;
}

.switch::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease;
}

.switch.on {
  background: linear-gradient(135deg, #4d80ff, #67a0ff);
}

.switch.on::after {
  transform: translateX(12px);
}

.table-wrap {
  overflow: auto;
}

table {
  width: 100%;
  min-width: 1080px;
  border-collapse: collapse;
  font-size: 14px;
}

.table-compact {
  min-width: 920px;
}

th,
 td {
  padding: 13px 12px;
  text-align: left;
  white-space: nowrap;
  border-bottom: 1px solid #f0f1f5;
}

thead th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: #fff;
  color: #4f5668;
  font-weight: 500;
}

.summary-row {
  background: #fff6fa;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 8px;
  border-radius: 50%;
}

.status-dot.green { background: #2eb67d; }
.status-dot.orange { background: #f3a31b; }
.status-dot.gray { background: #adb4c2; }

.editable-cell {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.icon-button,
.tiny-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: 1px solid transparent;
  border-radius: 12px;
  background: none;
  color: #8d93a6;
}

.metric-tip {
  width: 15px;
  height: 15px;
  margin-left: 4px;
  border: 1px solid #d1d5e0;
  border-radius: 50%;
  color: #9ea4b5;
  font-size: 11px;
}

.sortable {
  display: inline-flex;
  align-items: center;
  gap: 1px;
  border: none;
  background: none;
  color: inherit;
}

.sortable.active,
.edit-link {
  color: #2d63d8;
}

.sort-arrow {
  font-size: 10px;
  color: #a0a6b6;
}

.sort-arrow.active {
  color: var(--brand);
}

.ab-layout {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
}

.ab-preview {
  padding: 16px;
  border: 1px solid #f2d9e6;
  border-radius: 18px;
  background: linear-gradient(180deg, #fff9fc, #fff);
}

.ab-preview h4,
.section-title {
  margin: 0;
}

.stats-panel {
  grid-template-columns: repeat(auto-fit, minmax(132px, 1fr));
  margin-top: 8px;
}

.stats-card {
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: linear-gradient(180deg, #fff, #fff8fc);
}

.label {
  margin-bottom: 8px;
  color: var(--muted);
  font-size: 12px;
}

.stats-card strong {
  font-size: 18px;
}

.chart-panel {
  padding: 20px 16px 16px;
}

.line-chart {
  width: 100%;
  height: 260px;
}

.chart-grid {
  stroke: #eceef5;
  stroke-width: 1;
}

.chart-line {
  fill: none;
  stroke: #e24b8d;
  stroke-width: 3;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.chart-line-alt {
  stroke: #5c84ff;
}

.chart-dot {
  fill: #e24b8d;
}

.chart-dot-alt {
  fill: #5c84ff;
}

.chart-axis {
  display: grid;
  grid-template-columns: repeat(8, minmax(0, 1fr));
  gap: 8px;
  margin-top: 10px;
  color: #8c92a2;
  font-size: 12px;
}

.legend-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 6px;
  border-radius: 50%;
  background: #e24b8d;
}

.legend-dot-alt {
  background: #5c84ff;
}

.diff-text.up {
  color: #1ea65b;
}

.diff-text.down {
  color: #d45a5a;
}

.ab-meta {
  display: grid;
  gap: 6px;
  color: #5e6474;
}

.ab-overview {
  padding-bottom: 8px;
}

.menu-mask {
  position: fixed;
  inset: 0;
  z-index: 20;
}

.menu-panel {
  position: fixed;
  min-width: 144px;
  padding: 8px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 24px 80px rgba(25, 29, 43, 0.16);
}

.menu-panel button {
  width: 100%;
  min-height: 34px;
  border: none;
  border-radius: 10px;
  background: none;
  color: #475066;
  text-align: left;
}

.menu-panel button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.toast-stack {
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 60;
  flex-direction: column;
  align-items: stretch;
}

.toast {
  min-width: 220px;
  padding: 12px 14px;
  border-radius: 14px;
  color: #fff;
  background: rgba(31, 36, 48, 0.92);
  box-shadow: 0 18px 40px rgba(18, 22, 34, 0.22);
}

.toast.success { background: rgba(46, 182, 125, 0.96); }
.toast.error { background: rgba(239, 83, 80, 0.96); }

.empty-state {
  padding: 36px 20px;
  color: #8b92a5;
  text-align: center;
}

@media (max-width: 1100px) {
  .traffic-app {
    grid-template-columns: 72px 1fr;
  }

  .brand span:not(.brand-badge),
  .nav-label,
  .nav-arrow,
  .nav-sublist {
    display: none;
  }

  .brand,
  .nav-item,
  .nav-subitem {
    justify-content: center;
  }

  .pid-filter-grid,
  .report-filter-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 820px) {
  .traffic-app {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }

  .page {
    padding: 16px;
  }

  .form-grid,
  .ab-layout,
  .pid-filter-grid,
  .report-filter-grid {
    grid-template-columns: 1fr;
  }

  .chart-axis {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
</style>
