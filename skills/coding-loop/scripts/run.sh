#!/bin/bash
# coding-loop - 基于AI编程经验总结的循环编程脚本

# 默认参数
MAX_LOOPS=20
RESUME=false
CHECK_PROGRESS=true
TASK=""
MODEL="MiniMax-M2.1"
PROJECT_DIR=""

# State file lives in a user-owned directory. A shared /tmp path would let
# any local user pre-seed a state file; combined with the historical `source`
# load, that would be arbitrary code execution on the next --resume run.
STORAGE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/coding-loop"
mkdir -p "$STORAGE_DIR" 2>/dev/null
chmod 700 "$STORAGE_DIR" 2>/dev/null || true
STORAGE_FILE="$STORAGE_DIR/state"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-loops)
            MAX_LOOPS="$2"
            shift 2
            ;;
        --resume)
            RESUME=true
            shift
            ;;
        --check-progress)
            CHECK_PROGRESS=true
            shift
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --project)
            PROJECT_DIR="$2"
            shift 2
            ;;
        *)
            if [[ "$1" == "--"* ]]; then
                shift
            else
                TASK="$1"
                shift
            fi
            ;;
    esac
done

# 如果没有提供任务，提示用户
if [ -z "$TASK" ]; then
    echo "用法: coding-loop [选项] <编程任务>"
    echo ""
    echo "选项:"
    echo "  --max-loops N    最大循环次数 (默认: 20)"
    echo "  --model MODEL    使用的AI模型 (默认: MiniMax-M2.1)"
    echo "  --project DIR    项目目录 (默认: 当前目录)"
    echo "  --check-progress 启用进度检查"
    echo "  --resume        恢复之前的会话"
    echo ""
    echo "示例:"
    echo "  coding-loop 创建一个Python Web服务器"
    echo "  coding-loop --max-loops 10 --model MiniMax-M2.5 实现用户认证"
    echo "  coding-loop --project /path/to/project 优化前端页面"
    exit 1
fi

# 设置项目目录
if [ -z "$PROJECT_DIR" ]; then
    PROJECT_DIR="$(pwd)"
fi

# 加载编程经验
EXPERIENCE_FILE="/root/.openclaw/workspace/AI编程经验总结.md"

# 打印开始信息
echo "========================================"
echo "🔄 循环编程开始"
echo "========================================"
echo "任务: $TASK"
echo "最大循环: $MAX_LOOPS"
echo "使用模型: $MODEL"
echo "项目目录: $PROJECT_DIR"
echo ""

# 初始化变量
LOOP_COUNT=0
LAST_PROGRESS=""
NO_PROGRESS_COUNT=0
CREATED_FILES=()
MODIFIED_FILES=()

# 保存状态到文件
save_state() {
    umask 077
    cat > "$STORAGE_FILE" << EOF
LOOP_COUNT=$LOOP_COUNT
LAST_PROGRESS=$LAST_PROGRESS
NO_PROGRESS_COUNT=$NO_PROGRESS_COUNT
TASK=$TASK
MODEL=$MODEL
PROJECT_DIR=$PROJECT_DIR
EOF
}

# 恢复状态 — parse known keys only; never `source` the file so a pre-seeded
# state file cannot execute arbitrary commands in this shell.
restore_state() {
    if [ ! -f "$STORAGE_FILE" ]; then
        return
    fi
    local line key value
    while IFS= read -r line || [ -n "$line" ]; do
        key="${line%%=*}"
        value="${line#*=}"
        case "$key" in
            LOOP_COUNT)        LOOP_COUNT="$value" ;;
            LAST_PROGRESS)     LAST_PROGRESS="$value" ;;
            NO_PROGRESS_COUNT) NO_PROGRESS_COUNT="$value" ;;
            TASK)              TASK="$value" ;;
            MODEL)             MODEL="$value" ;;
            PROJECT_DIR)       PROJECT_DIR="$value" ;;
        esac
    done < "$STORAGE_FILE"
    echo "📂 恢复会话: 第$LOOP_COUNT轮"
}

# 检查进度
check_progress() {
    if [ "$CHECK_PROGRESS" = true ]; then
        # 检测文件变化
        CURRENT_FILES=$(find "$PROJECT_DIR" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.vue" -o -name "*.react*" \) -mmin -5 2>/dev/null | wc -l)
        
        if [ "$CURRENT_FILES" != "$LAST_PROGRESS" ]; then
            echo "  📈 进度: 检测到文件变化"
            NO_PROGRESS_COUNT=0
            LAST_PROGRESS="$CURRENT_FILES"
            return 0
        else
            echo "  ⚠️ 无进展 (连续: $NO_PROGRESS_COUNT/3)"
            NO_PROGRESS_COUNT=$((NO_PROGRESS_COUNT + 1))
            return 1
        fi
    fi
    return 0
}

# 验证结果
verify_result() {
    echo "  🔍 验证中..."
    # 检查是否有语法错误
    local errors=0
    
    # Python 语法检查
    if command -v python3 &> /dev/null; then
        find "$PROJECT_DIR" -name "*.py" -type f -exec python3 -m py_compile {} \; 2>/dev/null || errors=$((errors + 1))
    fi
    
    # Node.js 语法检查
    if command -v node &> /dev/null; then
        find "$PROJECT_DIR" -name "*.js" -type f ! -path "*/node_modules/*" -exec node --check {} \; 2>/dev/null || errors=$((errors + 1))
    fi
    
    if [ $errors -eq 0 ]; then
        echo "  ✅ 验证通过"
        return 0
    else
        echo "  ⚠️ 发现 $errors 个潜在问题"
        return 1
    fi
}

# 选择模型 (根据任务复杂度)
select_model() {
    local task="$1"
    local length=${#task}
    
    if [ $length -gt 100 ]; then
        echo "MiniMax-M2.5"
    else
        echo "MiniMax-M2.1"
    fi
}

# 恢复会话 (如果需要)
if [ "$RESUME" = true ]; then
    restore_state
fi

# 主循环
while [ $LOOP_COUNT -lt $MAX_LOOPS ]; do
    LOOP_COUNT=$((LOOP_COUNT + 1))
    
    # 保存当前状态
    save_state
    
    echo "📍 第${LOOP_COUNT}轮 (模型: $MODEL):"
    
    # 执行编程任务 (这里调用 AI 编程)
    # 实际使用时替换为具体的 AI 调用
    echo "  🤖 正在执行编程任务..."
    sleep 2
    
    # 检查进度
    if ! check_progress; then
        if [ $NO_PROGRESS_COUNT -ge 3 ]; then
            echo ""
            echo "🛑 触发熔断器: 连续3次无进展，停止循环"
            break
        fi
    fi
    
    # 验证结果
    verify_result
    
    # 检查是否人为停止 (模拟)
    if [ $LOOP_COUNT -ge 2 ]; then
        # 在实际使用中，这里会检查是否收到完成信号
        :
    fi
    
    echo ""
done

# 超出最大循环
if [ $LOOP_COUNT -ge $MAX_LOOPS ]; then
    echo "⚠️ 达到最大循环次数 ($MAX_LOOPS)，退出"
fi

# 生成总结报告
echo ""
echo "========================================"
echo "📊 循环编程完成报告"
echo "========================================"
echo "总轮数: $LOOP_COUNT"
echo "任务: $TASK"
echo "模型: $MODEL"
echo ""

# 清理
rm -f "$STORAGE_FILE"
