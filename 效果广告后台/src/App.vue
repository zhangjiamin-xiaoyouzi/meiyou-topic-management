<template>
  <div class="page-shell">
    <div class="page-header">
      <div class="breadcrumb">流量管理 / 溯流管理</div>
      <div class="scene-box">
        <label>广告场景：</label>
        <select v-model="selectedScene">
          <option v-for="scene in scenes" :key="scene.id" :value="scene.id">{{ scene.label }}</option>
        </select>
      </div>
    </div>

    <section class="panel groups-panel">
      <div class="panel-title">
        <span>分组管理</span>
        <button class="primary-button" @click="addGroup">+ 添加分组</button>
      </div>
      <div class="group-tabs">
        <button
          v-for="group in groups"
          :key="group.id"
          :class="['group-tab', { active: group.id === activeGroupId } ]"
          @click="setActiveGroup(group.id)">
          {{ group.title }}
        </button>
        <button class="ab-button" @click="createAbTest">创建A/B测试</button>
      </div>
      <div class="group-info" v-if="activeGroup">
        <div class="group-info-row">
          <span class="label">广告位：</span>
          <span>{{ activeGroup.adSlot }}</span>
        </div>
        <div class="group-info-row">
          <span class="label">分组规则：</span>
          <span>{{ activeGroup.rule }}</span>
        </div>
        <div class="group-switch">
          <span>分组开关</span>
          <label class="toggle-switch">
            <input type="checkbox" v-model="activeGroup.enabled" />
            <span class="slider"></span>
          </label>
        </div>
      </div>
    </section>

    <section class="panel source-panel">
      <div class="panel-title">
        <span>DSP来源</span>
        <button class="primary-button" @click="addDspSource">+ 添加DSP来源</button>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>操作</th>
              <th>DSP来源</th>
              <th>状态</th>
              <th>定价方式</th>
              <th>平台</th>
              <th>价格</th>
              <th>千人均收益</th>
              <th>预估收入</th>
              <th>eCPM</th>
              <th>千次请求价值</th>
              <th>请求量</th>
              <th>返回率</th>
              <th>竞价成功数</th>
              <th>竞价成功率</th>
              <th>展示量</th>
              <th>竞价展示率</th>
              <th>点击率</th>
              <th>cpc</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in visibleSources" :key="item.id">
              <td>
                <button class="link-button" @click="editDsp(item)">编辑</button>
              </td>
              <td>{{ item.name }}</td>
              <td>
                <label class="toggle-switch small">
                  <input type="checkbox" v-model="item.enabled" />
                  <span class="slider"></span>
                </label>
              </td>
              <td><span class="tag">{{ item.pricing }}</span></td>
              <td>{{ item.platform }}</td>
              <td>
                <div class="price-input">
                  <input type="text" v-model="item.price" @blur="normalizePrice(item)" />
                </div>
              </td>
              <td>{{ item.rpm }}</td>
              <td>{{ item.income }}</td>
              <td>{{ item.ecpm }}</td>
              <td>{{ item.reqk }}</td>
              <td>{{ item.request }}</td>
              <td>{{ item.responseRate }}</td>
              <td>{{ item.wins }}</td>
              <td>{{ item.winRate }}</td>
              <td>{{ item.impressions }}</td>
              <td>{{ item.showRate }}</td>
              <td>{{ item.ctr }}</td>
              <td>{{ item.cpc }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="disabled-summary" @click="toggleShowDisabled">
        <span>{{ disabledCount }} 个DSP来源未启用</span>
        <span class="toggle-text">{{ showDisabled ? '收起' : '展开' }}</span>
      </div>
      <div class="disabled-list" v-if="showDisabled">
        <div v-for="item in disabledSources" :key="item.id" class="disabled-item">
          <span>{{ item.name }}</span>
          <span>{{ item.platform }}</span>
          <span>{{ item.pricing }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      selectedScene: 'all',
      scenes: [
        { id: 'all', label: '请选择广告场景' },
        { id: 'scene1', label: '广告场景1' },
        { id: 'scene2', label: '广告场景2' }
      ],
      groups: [
        { id: 1, title: '1-分组测试1', adSlot: '2101-美艳-竖版-横屏', rule: '身份 包含 变量', enabled: true },
        { id: 2, title: '2-分组测试2', adSlot: '2101-美艳-竖版-横屏', rule: '身份 包含 变量', enabled: true },
        { id: 3, title: '默认-默认分组', adSlot: '2101-美艳-竖版-横屏', rule: '身份 包含 变量', enabled: false }
      ],
      activeGroupId: 1,
      dspSources: [
        { id: 1, name: 'MY-嗨量', enabled: true, pricing: '竞价', platform: '安卓', price: '12.50', rpm: '¥0.08', income: '8,560.3', estimate: '¥18.25', ecpm: '¥0.68', reqk: '9.8万', request: '31.5万', responseRate: '52.6%', wins: '3.1万', winRate: '23.0%', impressions: '12.5万', showRate: '100.0%', ctr: '4.3%', cpc: '¥1.24' },
        { id: 2, name: 'MY-TapTap-安卓', enabled: true, pricing: '定价', platform: '安卓', price: '15.80', rpm: '¥0.07', income: '12,890.5', estimate: '¥16.78', ecpm: '¥0.72', reqk: '14.5万', request: '53.0%', responseRate: '0', wins: '0', winRate: '0.0%', impressions: '5.5万', showRate: '100.0%', ctr: '4.0%', cpc: '¥1.58' },
        { id: 3, name: 'MY-佳投', enabled: true, pricing: '竞价', platform: '安卓', price: '8.90', rpm: '¥0.06', income: '5,420.2', estimate: '¥14.56', ecpm: '¥0.45', reqk: '7.2万', request: '51.7%', responseRate: '1.2万', wins: '33.3%', winRate: '2.8万', impressions: '100.0%', showRate: '4.0%', ctr: '¥0.89', cpc: '---' }
      ],
      showDisabled: false
    }
  },
  computed: {
    activeGroup() {
      return this.groups.find(group => group.id === this.activeGroupId)
    },
    disabledSources() {
      return this.dspSources.filter(item => !item.enabled)
    },
    disabledCount() {
      return this.disabledSources.length
    },
    visibleSources() {
      return this.dspSources
    }
  },
  methods: {
    setActiveGroup(id) {
      this.activeGroupId = id
    },
    addGroup() {
      const nextId = this.groups.length + 1
      this.groups.push({ id: nextId, title: `${nextId}-分组测试${nextId}`, adSlot: '2101-美艳-竖版-横屏', rule: '身份 包含 变量', enabled: true })
      this.activeGroupId = nextId
    },
    addDspSource() {
      const nextId = this.dspSources.length + 1
      this.dspSources.push({ id: nextId, name: `MY-新增来源${nextId}`, enabled: true, pricing: '竞价', platform: '安卓', price: '9.00', rpm: '¥0.05', income: '0.0', estimate: '¥0.00', ecpm: '¥0.00', reqk: '0', request: '0', responseRate: '0%', wins: '0', winRate: '0%', impressions: '0', showRate: '0%', ctr: '0%', cpc: '¥0.00' })
    },
    editDsp(item) {
      window.alert(`编辑 DSP 来源：${item.name}`)
    },
    createAbTest() {
      window.alert('创建A/B测试功能已触发')
    },
    normalizePrice(item) {
      const value = parseFloat(item.price)
      if (!Number.isNaN(value)) {
        item.price = value.toFixed(2)
      }
    },
    toggleShowDisabled() {
      this.showDisabled = !this.showDisabled
    }
  }
}
</script>

<style>
:root {
  color-scheme: light;
  font-family: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}
body {
  margin: 0;
  background: #f5f7fb;
}
.page-shell {
  max-width: 1600px;
  margin: 24px auto;
  padding: 0 24px 40px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.breadcrumb {
  font-size: 14px;
  color: #2a2a2a;
}
.scene-box {
  display: flex;
  align-items: center;
  gap: 10px;
}
.scene-box label {
  color: #2a2a2a;
}
.scene-box select {
  min-width: 220px;
  height: 34px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 12px;
  background: #fff;
}
.panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
  padding: 20px;
  margin-bottom: 20px;
}
.panel-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.panel-title span {
  font-size: 16px;
  color: #303133;
  font-weight: 600;
}
.primary-button,
.ab-button {
  border: 1px solid #ff4d70;
  background: #fff;
  color: #ff4d70;
  height: 34px;
  padding: 0 14px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.primary-button:hover,
.ab-button:hover {
  background: #ff4d70;
  color: #fff;
}
.group-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}
.group-tab {
  min-width: 120px;
  padding: 8px 14px;
  border-radius: 18px;
  border: 1px solid #dcdfe6;
  background: #fff;
  color: #606266;
  cursor: pointer;
}
.group-tab.active {
  background: #faf0f4;
  border-color: #ff4d70;
  color: #ff4d70;
}
.ab-button {
  margin-left: auto;
}
.group-info {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  align-items: center;
  margin-top: 18px;
}
.group-info-row {
  display: flex;
  gap: 8px;
  color: #4a4a4a;
  line-height: 1.75;
}
.group-info-row .label {
  color: #909399;
}
.group-switch {
  display: flex;
  align-items: center;
  gap: 10px;
}
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 24px;
}
.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-switch .slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background-color: #dcdfe6;
  border-radius: 999px;
  transition: 0.2s;
}
.toggle-switch .slider::before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: #fff;
  border-radius: 50%;
  transition: 0.2s;
}
.toggle-switch input:checked + .slider {
  background-color: #3f8cff;
}
.toggle-switch input:checked + .slider::before {
  transform: translateX(22px);
}
.toggle-switch.small {
  width: 36px;
  height: 20px;
}
.toggle-switch.small .slider::before {
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
}
.table-wrap {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1600px;
}
th, td {
  padding: 12px 10px;
  border-bottom: 1px solid #eff2f6;
  text-align: left;
  white-space: nowrap;
  font-size: 13px;
  color: #606266;
}
th {
  background: #f7f9fc;
  color: #909399;
  font-weight: 600;
}
.link-button {
  border: none;
  background: none;
  color: #409eff;
  cursor: pointer;
  padding: 0;
}
.tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  border-radius: 12px;
  background: #f0f9ff;
  color: #409eff;
  font-size: 12px;
}
.price-input input {
  width: 70px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 4px 8px;
  text-align: right;
}
.disabled-summary {
  margin-top: 10px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #606266;
  font-size: 13px;
}
.disabled-list {
  margin-top: 10px;
  padding: 12px 14px;
  background: #f8f9fb;
  border-radius: 8px;
}
.disabled-item {
  display: flex;
  gap: 16px;
  padding: 6px 0;
}
.toggle-text {
  color: #409eff;
}
</style>
