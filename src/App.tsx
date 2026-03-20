import { useState } from 'react';
import { Dog, Stethoscope, Camera, AlertCircle, CheckCircle, Clock, Heart } from 'lucide-react';

interface PredictionResult {
  success: boolean;
  disease: string;
  confidence: number;
  description: string;
  care_tips: string[];
  severity: string;
  error?: string;
}

function SeverityBadge({ severity }: { severity: string }) {
  const colorMap: Record<string, string> = {
    'Critical': 'bg-red-100 text-red-800 border-red-200',
    'Critical Emergency': 'bg-red-100 text-red-800 border-red-200',
    'Serious': 'bg-orange-100 text-orange-800 border-orange-200',
    'Moderate': 'bg-yellow-100 text-yellow-800 border-yellow-200',
    'Moderate to Serious': 'bg-orange-100 text-orange-800 border-orange-200',
    'Mild to Moderate': 'bg-blue-100 text-blue-800 border-blue-200',
    'None': 'bg-green-100 text-green-800 border-green-200',
    'Unknown': 'bg-gray-100 text-gray-800 border-gray-200',
  };
  const color = colorMap[severity] || 'bg-gray-100 text-gray-800 border-gray-200';
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-semibold border ${color}`}>
      {severity}
    </span>
  );
}

function ResultCard({ result }: { result: PredictionResult }) {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 mt-6 border border-gray-100">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-800">{result.disease}</h3>
          <div className="flex items-center gap-2 mt-1">
            <SeverityBadge severity={result.severity} />
            <span className="text-sm text-gray-500">
              {result.confidence.toFixed(1)}% confidence
            </span>
          </div>
        </div>
        <div className="w-16 h-16 rounded-full bg-indigo-50 flex items-center justify-center">
          <span className="text-2xl font-bold text-indigo-600">{Math.round(result.confidence)}%</span>
        </div>
      </div>
      <p className="text-gray-600 mb-4 text-sm leading-relaxed">{result.description}</p>
      <div>
        <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-1">
          <Heart size={16} className="text-rose-500" />
          Care Tips
        </h4>
        <ul className="space-y-1">
          {result.care_tips.map((tip, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
              <CheckCircle size={14} className="text-green-500 mt-0.5 flex-shrink-0" />
              {tip}
            </li>
          ))}
        </ul>
      </div>
      <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
        <p className="text-xs text-amber-700 flex items-start gap-1">
          <AlertCircle size={14} className="flex-shrink-0 mt-0.5" />
          <span>This is for informational purposes only. Always consult a licensed veterinarian for proper diagnosis and treatment.</span>
        </p>
      </div>
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'symptom' | 'image'>('symptom');
  const [symptoms, setSymptoms] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSymptomSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!symptoms.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const res = await fetch('/predict-symptom', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms }),
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else setResult(data);
    } catch (err) {
      setError('Failed to connect to server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => setImagePreview(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const handleImageSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageFile) return;
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      const res = await fetch('/predict-image', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else setResult(data);
    } catch (err) {
      setError('Failed to connect to server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <header className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-3">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center">
            <Dog size={22} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800">AI Dog Health Diagnosis</h1>
            <p className="text-xs text-gray-500">ML-powered health assessment for your dog</p>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div className="flex border-b border-gray-100">
            <button
              onClick={() => { setActiveTab('symptom'); setResult(null); setError(null); }}
              className={`flex-1 py-4 px-6 flex items-center justify-center gap-2 font-medium transition-colors ${
                activeTab === 'symptom'
                  ? 'bg-indigo-50 text-indigo-700 border-b-2 border-indigo-600'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Stethoscope size={18} />
              Symptom Analysis
            </button>
            <button
              onClick={() => { setActiveTab('image'); setResult(null); setError(null); }}
              className={`flex-1 py-4 px-6 flex items-center justify-center gap-2 font-medium transition-colors ${
                activeTab === 'image'
                  ? 'bg-indigo-50 text-indigo-700 border-b-2 border-indigo-600'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Camera size={18} />
              Image Detection
            </button>
          </div>

          <div className="p-6">
            {activeTab === 'symptom' ? (
              <form onSubmit={handleSymptomSubmit}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Describe your dog's symptoms
                </label>
                <textarea
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  placeholder="e.g., lethargy, vomiting, loss of appetite, coughing..."
                  rows={4}
                  className="w-full border border-gray-200 rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 resize-none"
                />
                <p className="text-xs text-gray-400 mt-1 mb-4">
                  Enter symptoms separated by commas for best results.
                </p>
                <button
                  type="submit"
                  disabled={loading || !symptoms.trim()}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Clock size={16} className="animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Stethoscope size={16} />
                      Analyze Symptoms
                    </>
                  )}
                </button>
              </form>
            ) : (
              <form onSubmit={handleImageSubmit}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload a photo of your dog
                </label>
                <div
                  className="border-2 border-dashed border-gray-200 rounded-xl p-8 text-center cursor-pointer hover:border-indigo-300 transition-colors"
                  onClick={() => document.getElementById('imageInput')?.click()}
                >
                  {imagePreview ? (
                    <img src={imagePreview} alt="Preview" className="max-h-48 mx-auto rounded-lg object-contain" />
                  ) : (
                    <div>
                      <Camera size={40} className="mx-auto text-gray-300 mb-2" />
                      <p className="text-sm text-gray-500">Click to upload an image</p>
                      <p className="text-xs text-gray-400 mt-1">PNG, JPG, GIF up to 16MB</p>
                    </div>
                  )}
                </div>
                <input
                  id="imageInput"
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                />
                <button
                  type="submit"
                  disabled={loading || !imageFile}
                  className="w-full mt-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Clock size={16} className="animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Camera size={16} />
                      Analyze Image
                    </>
                  )}
                </button>
              </form>
            )}

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-2">
                <AlertCircle size={16} className="text-red-500 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {result && <ResultCard result={result} />}
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { icon: Stethoscope, title: 'Symptom Analysis', desc: 'Describe symptoms in plain text and get instant disease predictions using machine learning.' },
            { icon: Camera, title: 'Image Detection', desc: 'Upload a photo to detect skin conditions, ticks, and other visible health issues.' },
            { icon: Heart, title: '24 Conditions', desc: 'Our system can identify over 20 common dog health conditions with care recommendations.' },
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
              <div className="w-8 h-8 bg-indigo-50 rounded-lg flex items-center justify-center mb-2">
                <Icon size={16} className="text-indigo-600" />
              </div>
              <h3 className="font-semibold text-gray-800 text-sm mb-1">{title}</h3>
              <p className="text-xs text-gray-500 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
