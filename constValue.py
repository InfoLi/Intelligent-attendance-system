# 用于设置html渲染模板数组

todayCheck = '<div class="sign">' \
             '实际打卡时间：' \
             '<span class="sign-time" style="padding-right: 20%;" id="timeFlow#0">#1（#2）</span>' \
             '<button class="layui-btn layui-btn-primary">#3</button>' \
             '</div>'

adminOA_html = '<tbody>' \
               '<tr>' \
               '<td>#1</td>' \
               '<td>#2</td>' \
               '<td>#3</td>' \
               '<td>#4</td>' \
               '<td>#5</td>' \
               '<td><a onclick="queryApply(#6)">点击审批</a></td>' \
               '</tr>' \
               '</tbody>'

applyLog_html = '{' \
                '"id": "#1"' \
                ',"class": "#2"' \
                ',"start time": "#3"' \
                ',"end time": "#4"' \
                ',"apply time": "#5"' \
                '},'

applyLog_html_before = 'table.render({' \
                       "elem: '#demo'" \
                       ',cols: [[ ' \
                       "{field: 'id', title: '申请人', width: 120,}" \
                       ",{field: 'class', title: '状态', width: 120}" \
                       ",{field: 'start time', title: '开始时间', midWidth: 150}" \
                       ",{field: 'end time', title: '结束时间', midWidth: 160}" \
                       ",{field: 'apply time', title: '申请时间', midWidth: 160,sort: true}" \
                       ",{field: 'operation', title: '操作',toolbar:'#bar', width: 160}" \
                       ']]' \
                       ',data: ['

applyLog_html_after = ']' \
                      ',even: true' \
                      ',page: true ' \
                      ',limit: 10' \
                      '});'

generalWeek_html = '{' \
                   '"time": "#1"' \
                   ', "state": "#2"' \
                   ', "cause": "#3"' \
                   '},'

pendApply_html = '{' \
                 '"id": "#1"' \
                 ',"class": "#2"' \
                 ',"start time": "#3"' \
                 ',"end time": "#4"' \
                 ',"apply time": "#5"' \
                 '},'

personMonth_html = '{' \
                   '"id": "#1",' \
                   '"username": "#2",' \
                   '"position": "#3",' \
                   '"department": "#4",' \
                   '"number-attendance": "#5",' \
                   '"late": "#6",' \
                   '"leave-early": "#7"' \
                   '}'

personRange_html = '{' \
                   '"id":"#1",' \
                   '"username":"#2",' \
                   '"position":"#3",' \
                   '"date":"#4",' \
                   '"classes":"#5",' \
                   '"check-in-time":"#6",' \
                   '"state":#7"' \
                   '}'


homePend_html = '{' \
      '"id": "#1"' \
      ',"username": "#2"' \
      ',"affair": "事假"' \
      ',"state": "#3"' \
    '},'

adminSearch_html = '{' \
          '"id": "#1"' \
          ', "username": "#2"' \
          ', "sex": "#3"' \
          ', "position": "#4"' \
          ', "department": "#5"' \
        '}'