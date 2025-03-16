export const generateMacro = async (description, job, level) => {
  const response = await fetch('http://localhost:8000/api/macro/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      description,
      job,
      level
    }),
  });

  if (!response.ok) {
    throw new Error('生成失败');
  }
  const data = await response.json();
  return data.macro;
};
