import React, { useState } from 'react';
import { generateMacro } from '../api/macroApi';

export default function MacroGenerator() {
  const [input, setInput] = useState('');
  const [job, setJob] = useState('白魔导士');
  const [level, setLevel] = useState(90);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const macro = await generateMacro(input, job, level);
      setResult(macro);
    } catch (error) {
      alert('生成失败: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <div className="macro-generator">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>职业选择：</label>
          <select value={job} onChange={(e) => setJob(e.target.value)}>
            <option value="白魔导士">白魔导士</option>
            <option value="黑魔导士">黑魔导士</option>
            <option value="战士">战士</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>角色等级：</label>
          <input 
            type="number" 
            value={level}
            onChange={(e) => setLevel(e.target.value)}
            min="1" 
            max="90" 
          />
        </div>

        <div className="form-group">
          <label>需求描述：</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="例：需要开场爆发循环，包含群体治疗..."
            rows="4"
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? '生成中...' : '生成宏'}
        </button>
      </form>

      {result && (
        <div className="result-area">
          <h3>生成的宏命令：</h3>
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
}
