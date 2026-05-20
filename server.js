import express from 'express';
import mysql from 'mysql2/promise';
import cors from 'cors';
const app = express();

// 数据库配置
const dbConfig = {
  host: 'localhost',     // 数据库地址（本地一般是localhost）
  user: 'root', // 比如root
  password: '1234',
  database: 'check_class',  // 比如battlefield_injury
  charset: 'utf8mb4'
};

// 允许跨域 + 解析JSON请求
app.use(cors());
app.use(express.json());

// 核心接口：根据伤情名称（injury_type）查询处置建议
app.post('/api/battlefield/treatment', async (req, res) => {
  try {
    const { injury } = req.body; // 前端传过来的伤情名称，比如“头皮裂伤”
    if (!injury) {
      return res.status(400).json({ 
        code: 400, 
        message: '请传入伤情名称' 
      });
    }

    // 连接数据库查询
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute(
      `SELECT classification, description 
       FROM war_injuries
       WHERE injury_type = ? 
       ORDER BY id`,  // 按id排序，保持数据顺序和你插入的一致
      [injury]
    );
    await connection.end();

    // 格式化数据：按classification（处置类型）分组，方便前端展示
    const result = {};
    rows.forEach(item => {
      const type = item.classification;
      if (!result[type]) {
        result[type] = [];
      }
      result[type].push(item.description);
    });

    // 返回结果
    res.status(200).json({
      code: 200,
      message: '查询成功',
      injuryName: injury,
      instructions: result // 分组后的处置建议（比如{ "临床特点": [...], "急救": [...] }）
    });
  } catch (error) {
    console.error('查询失败：', error);
    res.status(500).json({ 
      code: 500, 
      message: '服务器内部错误' 
    });
  }
});

// 启动服务（端口8090，和前端请求地址对应）
const PORT = 8090;
app.listen(PORT, () => {
  console.log(`服务已启动：http://localhost:${PORT}`);
});