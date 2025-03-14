"use client";
import { useEffect, useState } from "react";
import axios from "axios";

interface FormResponse {
    id: number;
    text1: string;
    text2: string;
    text3: string;
    file_path: string;
}

export default function ViewForms() {
    const [forms, setForms] = useState<FormResponse[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get("http://localhost:8000/get-forms/")
            .then(response => {
                console.log("✅ API Response:", response.data); // Debugging line
                setForms(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error("❌ Error fetching data:", error);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading data...</p>;

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold mb-4">Submitted Forms</h1>
            {forms.length === 0 ? (
                <p className="text-gray-500">No form submissions found.</p>
            ) : (
                <table className="w-full border-collapse border border-gray-300">
                    <thead>
                        <tr className="bg-gray-200">
                            <th className="border p-2">ID</th>
                            <th className="border p-2">Text 1</th>
                            <th className="border p-2">Text 2</th>
                            <th className="border p-2">Text 3</th>
                            <th className="border p-2">File</th>
                        </tr>
                    </thead>
                    <tbody>
                        {forms.map((form) => (
                            <tr key={form.id} className="text-center">
                                <td className="border p-2">{form.id}</td>
                                <td className="border p-2">{form.text1}</td>
                                <td className="border p-2">{form.text2}</td>
                                <td className="border p-2">{form.text3}</td>
                                <td className="border p-2">
                                    {form.file_path ? (
                                        <a href={`http://localhost:8000/${form.file_path}`} target="_blank" rel="noopener noreferrer" className="text-blue-500">
                                            View File
                                        </a>
                                    ) : (
                                        "No file"
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
